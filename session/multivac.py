import redis

import matplotlib.pyplot as plt

from agents.agent_registry import AGENTS
from buffers.action_buffer import ActionBuffer
from buffers.observation_buffer import ObservationBuffer
from environment.environment_registry import ENVIRONMENTS


DEFAULT_IMAGE_HEIGHT = 100
DEFAULT_IMAGE_WIDTH = 50


class Multivac:
    """
    The Multivac class starts an environment and an agent in that environment.
    """

    def __init__(self, environment_name, agent_name, num_training_steps, num_inference_steps, redis_port,
                 image_height=DEFAULT_IMAGE_HEIGHT, image_width=DEFAULT_IMAGE_WIDTH):
        """
        Initialize the Multivac.
        :param environment_name: Name of the environment to use.
        :param agent_name: Name of the agent being to use.
        :param num_training_steps: Number of steps to take during training of the agent.
        :param num_inference_steps: Number of steps to take after training, during inference to test the agent.
        :param redis_port: Port number that the redis server is running on. This is used to set up buffer objects.
        :param image_height: Height of the observation images. This is device dependent.
        :param image_width: Width of the observation images. This is device dependent.
        """
        # Start Redis connection on specified port.
        self.redis_client = redis.Redis(port=redis_port)

        action_buffer = ActionBuffer(self.redis_client)
        observation_buffer = ObservationBuffer(self.redis_client)

        self.environment = ENVIRONMENTS[environment_name](action_buffer, observation_buffer, image_height, image_width)
        self.agent = AGENTS[agent_name](self.environment)

        self.num_training_steps = num_training_steps
        self.num_inference_steps = num_inference_steps

    def launch(self):
        # First train the agent.
        print("Starting to train the agent.")
        self.agent.train(self.num_training_steps)

        print("Done training the agent.")

        print("Resetting the environment.")
        curr_obs = self.environment.reset()

        print("Starting to carry out inference for the agent.")

        total_reward = 0.0
        for step in range(self.num_inference_steps):
            action = self.agent.predict(curr_obs)
            curr_obs, reward, info = self.environment.step(action)
            rendered_img = self.environment.render()
            total_reward += reward

            plt.imshow(rendered_img)

        print("Done, now shutting down.")
        self.redis_client.shutdown()

        print("FINAL TOTAL REWARD: {}".format(total_reward))
        print("FINAL AVERAGE REWARD: {}".format(total_reward / self.num_inference_steps))
