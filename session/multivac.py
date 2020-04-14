import cv2
import logging
import matplotlib.pyplot as plt
import numpy as np
import os
import redis

from agents.agent_registry import AGENTS
from buffers.action_buffer import ActionBuffer
from buffers.observation_buffer import ObservationBuffer
from environment.android_device_env import AndroidDeviceEnv
from environment.environment_registry import ENVIRONMENTS


# Height for text portion of the video frame.
TEXT_HEIGHT = 100

# Base path for outputting recordings. Note: if you run two sessions with same agent and environment name, then
# any old videos will be replaced.
OUTPUT_RECORDING_BASE_PATH = "./out"


class Multivac:
    """
    The Multivac class starts an environment and an agent in that environment.
    """

    def __init__(self, environment_name, agent_name, num_steps, redis_port, video_fps=1, display_video=False):
        """
        Initialize the Multivac. This involves,
          1. Open a redis client and setting up an action and observation buffer. This establishes an exchange
             protocol between the Multivac and a ConnectionClient
          2. Gather an initial observation from the observation buffer to collect metadata information
          3. Initialize an environment and an agent in that environment
          4. Setup the video recorder and writer

        :param environment_name: Name of the environment to use.
        :param agent_name: Name of the agent to use.
        :param num_steps: Number of steps to take on the environment.
        :param redis_port: Port number that the redis server is running on. This is used to set up buffer objects.
        :param video_fps: frame per second of the output video. Each frame will be one observation image.
        :param display_video: Boolean flag indicating whether or not to display the video of the Gym environment during
                              execution.
        """

        self.logger = logging.getLogger("Multivac")
        self.logger.addHandler(logging.StreamHandler())
        self.logger.setLevel(logging.DEBUG)

        assert environment_name in ENVIRONMENTS, "{} is not a valid environment name".format(environment_name)
        assert agent_name in AGENTS, "{} is not a valid agent name".format(agent_name)

        # Start Redis connection on specified port.
        self.redis_client = redis.Redis(port=redis_port)

        action_buffer = ActionBuffer(self.redis_client)
        observation_buffer = ObservationBuffer(self.redis_client)

        # Stall until we get the first observation from the observation buffer to collect metadata
        self.logger.debug("Gathering initial image from observation buffer")
        initial_observation = observation_buffer.blocking_read_elem()
        initial_image_from_observation = AndroidDeviceEnv.process_image_from_observation(initial_observation)
        image_height, image_width, _ = initial_image_from_observation.shape

        self.logger.debug(
            "Device height: {}; Device width: {}".format(image_height, image_width)
        )

        self.environment = ENVIRONMENTS[environment_name](
            action_buffer,
            observation_buffer,
            image_height,
            image_width
        )

        self.agent = AGENTS[agent_name](self.environment)

        self.num_steps = num_steps

        self.display_video = display_video

        # Set up the video recorder.
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')

        if not os.path.exists(OUTPUT_RECORDING_BASE_PATH):
            os.mkdir(OUTPUT_RECORDING_BASE_PATH)

        output_recording_path = os.path.join(
            OUTPUT_RECORDING_BASE_PATH,
            "{}-{}.mp4".format(agent_name, environment_name)
        )

        self.video_writer = cv2.VideoWriter(
            output_recording_path,
            fourcc,
            float(video_fps),
            (image_width, image_height + TEXT_HEIGHT)
        )

    def launch(self):
        """
        Launch the agent on the environment.

        First, we reset the environment back to its original state and gather an initial observation.
        Once this is complete, the agent carries out num_steps actions on the environment. After each action,
        we record the observation image and render it to the user. At the end, we write the resulting video to disk.
        """

        # Reset the environment to its initial state. This also allows us to get an initial observation image.
        self.logger.info("Resetting the environment.")
        curr_obs = self.environment.reset()

        self.logger.info("Starting to carry out steps for the agent.")

        total_reward = 0.0
        self.process_rendered_img(0, total_reward)

        for step in range(1, self.num_steps + 1):
            action = self.agent.take_action(curr_obs)
            curr_obs, reward, info = self.environment.step(action)
            total_reward += reward
            self.process_rendered_img(step, total_reward / step)

        self.logger.info("FINAL TOTAL REWARD: {}".format(total_reward))
        self.logger.info("FINAL AVERAGE REWARD: {}".format(total_reward / self.num_steps))

        self.video_writer.release()

    def process_rendered_img(self, step_no, average_reward):
        """
        Display a rendered img from the environment along with writing it to disk as part of a video recording.
        :param step_no: total number of steps so far.
        :param average_reward: average reward so far.
        """

        # Gather rendered image.
        rendered_img = self.environment.render(mode='rgb_array')

        # Construct informational text.
        text_to_display = "{} | Step: {} | Average Reward: {:.2f}".format("MULTIVAC", step_no, average_reward)

        if self.display_video:
            # Display to user.
            plt.figure(3)
            plt.clf()
            plt.imshow(rendered_img)
            plt.title(text_to_display)
            plt.axis('off')
            plt.pause(0.05)

        # Write image as a single frame with informational text added on.
        text_img = np.full(shape=(TEXT_HEIGHT, rendered_img.shape[1], 3), fill_value=255, dtype=np.uint8)

        cv2.putText(
            img=text_img,
            text=text_to_display,
            org=(0, int(TEXT_HEIGHT / 2)),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=1,
            color=(0, 0, 0),
            thickness=2,
            lineType=2
        )

        full_img = np.concatenate([text_img, rendered_img])

        # OpenCV video writer requires image in BGR format
        full_img_bgr = cv2.cvtColor(full_img, cv2.COLOR_RGB2BGR)

        self.video_writer.write(full_img_bgr)
