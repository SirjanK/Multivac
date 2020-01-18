import matplotlib.pyplot as plt
import os
import redis

from cv2 import VideoWriter, VideoWriter_fourcc

from agents.agent_registry import AGENTS
from buffers.action_buffer import ActionBuffer
from buffers.observation_buffer import ObservationBuffer
from environment.environment_registry import ENVIRONMENTS


# These are the defaults for the Pixel 2 Emulator.
DEFAULT_IMAGE_HEIGHT = 1920
DEFAULT_IMAGE_WIDTH = 1080

# Base path for outputting recordings. Note: if you run two sessions with same agent and environment name, then
# any old videos will be replaced.
OUTPUT_RECORDING_BASE_PATH = "./out"


class Multivac:
    """
    The Multivac class starts an environment and an agent in that environment.
    """

    def __init__(self, environment_name, agent_name, num_training_steps, num_inference_steps, redis_port,
                 image_height=DEFAULT_IMAGE_HEIGHT, image_width=DEFAULT_IMAGE_WIDTH, video_fps=1):
        """
        Initialize the Multivac.
        :param environment_name: Name of the environment to use.
        :param agent_name: Name of the agent to use.
        :param num_training_steps: Number of steps to take during training of the agent.
        :param num_inference_steps: Number of steps to take after training, during inference to test the agent.
        :param redis_port: Port number that the redis server is running on. This is used to set up buffer objects.
        :param image_height: Height of the observation images. This is device dependent.
        :param image_width: Width of the observation images. This is device dependent.
        :param video_fps: frame per second of the output video. Each frame will be one observation image.
        """

        # Start Redis connection on specified port.
        self.redis_client = redis.Redis(port=redis_port)

        action_buffer = ActionBuffer(self.redis_client)
        observation_buffer = ObservationBuffer(self.redis_client)

        self.environment = ENVIRONMENTS[environment_name](action_buffer, observation_buffer, image_height, image_width)
        self.agent = AGENTS[agent_name](self.environment)

        self.num_training_steps = num_training_steps
        self.num_inference_steps = num_inference_steps

        # Set up the video recorder.
        fourcc = VideoWriter_fourcc(*'mp4v')

        if not os.path.exists(OUTPUT_RECORDING_BASE_PATH):
            os.mkdir(OUTPUT_RECORDING_BASE_PATH)

        output_recording_path = os.path.join(
            OUTPUT_RECORDING_BASE_PATH,
            "{}-{}.mp4".format(agent_name, environment_name)
        )

        self.video_writer = VideoWriter(output_recording_path, fourcc, float(video_fps), (image_width, image_height))

    def launch(self):
        """
        Launch the agent on the environment. Involves two phases:
          1. Training phase: Here, we train the agent for num_training_steps, and it is free to act on the
             environment as it chooses.
          2. Inference phase: Here, we test the agent for num_inference_steps. Before this, we reset the environment
             back to its original state and gather an initial observation. Once this is complete, agent carries out
             num_inference_steps actions on the environment. After each action, we record the observation image
             and render it to the user. At the end of the inference phase, we write the resulting video to disk.
        """

        # First train the agent.
        print("Starting to train the agent.")
        self.agent.train(self.num_training_steps)

        print("Done training the agent.")

        # Reset the environment to its initial state. This also allows us to get an initial observation image.
        print("Resetting the environment.")
        curr_obs = self.environment.reset()

        print("Starting to carry out inference for the agent.")

        total_reward = 0.0
        self.process_rendered_img(0)

        for step in range(1, self.num_inference_steps + 1):
            action = self.agent.predict(curr_obs)
            curr_obs, reward, info = self.environment.step(action)
            total_reward += reward
            self.process_rendered_img(step)

        print("FINAL TOTAL REWARD: {}".format(total_reward))
        print("FINAL AVERAGE REWARD: {}".format(total_reward / self.num_inference_steps))

        self.redis_client.shutdown()
        self.video_writer.release()

    def process_rendered_img(self, step_no):
        """
        Display a rendered img from the environment along with writing it to disk as part of a video recording.
        :param step_no: total number of steps so far.
        """

        # Display to user.
        rendered_img = self.environment.render(mode='rgb_array')
        plt.figure(3)
        plt.clf()
        plt.imshow(rendered_img)
        plt.title("%s | Step: %d" % ("MULTIVAC", step_no))
        plt.axis('off')
        plt.pause(0.05)

        # Write image as a single frame.
        self.video_writer.write(rendered_img)
