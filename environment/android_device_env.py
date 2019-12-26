import gym
import numpy as np

from abc import ABC
from io import StringIO
from PIL import Image

from eventobjects.action import Action, RESET_ACTION


class AndroidDeviceEnv(gym.Env, ABC):
    """
    The AndroidDeviceEnv implements the gym Env interface in order to interface
    with an Android device through the abstraction layers of the Action and Observation buffers.

    Each action is defined in a continuous 2D space, specifically a down and up action on some 2D coordinate.
    Each observation is a continuous RGB image.
    """

    metadata = {'render.modes': ['rgb_array']}

    # Predefined (RGB image)
    NUM_CHANNELS = 3

    def __init__(self, action_buffer, observation_buffer, image_height, image_width):
        """
        Initialize the environment.
        :param action_buffer: ActionBuffer object that the environment should populate
        :param observation_buffer: ObservationBuffer object that the environment uses to gather image observations.
        :param image_height: height of the image observation in terms of num pixels
        :param image_width: width of the image observation in terms of num pixels
        """
        super(AndroidDeviceEnv, self).__init__()

        self.action_buffer = action_buffer
        self.observation_buffer = observation_buffer
        self.num_steps = 0

        # This is set to None initially. It is set in either the step() or reset() fn and is used during rendering.
        self.most_recent_observation = None

        # 2D continuous grid
        self.action_space = gym.spaces.Box(
            low=np.array([0.0, 0.0]),
            high=np.array([image_height, image_width]),
            dtype=np.float32
        )

        # H x W x C where C is number of channels.
        self.observation_space = gym.spaces.Box(
            low=0,
            high=255,
            shape=[image_height, image_width, self.NUM_CHANNELS],
            dtype=np.uint8
        )

    def step(self, action):
        # Wrap the action from the action space into an Action object
        action_buffer_elem = Action(tuple(action))

        # Add the action into the action buffer
        self.action_buffer.put_elem(action_buffer_elem)

        # Get new observation once action has been taken.
        # This observation corresponds to the image once the action has been taken.
        new_observation = self.get_new_observation()

        # Increment the num_steps counter
        self.num_steps += 1

        # Compute reward
        reward_val = self.compute_reward(new_observation)

        # Reset most_recent_observation tracker
        self.most_recent_observation = new_observation

        log_info = {
            'num_steps': self.num_steps
        }

        return new_observation, reward_val, log_info

    def reset(self):
        self.num_steps = 0

        # First clear all elements from the buffers
        self.action_buffer.clearall()
        self.observation_buffer.clearall()

        # Send a 'reset' action to the ActionBuffer so that the initial observation can be sent.
        self.action_buffer.put_elem(RESET_ACTION)

        # Read initial response
        self.most_recent_observation = self.get_new_observation()

        return self.most_recent_observation

    def render(self, mode='human'):
        if not self.most_recent_observation:
            raise Exception("most_recent_observation has not been set to a valid image. " +
                            "Most likely cause is neither step() nor reset() has been called in advance.")
        if mode == 'rgb_array':
            return self.most_recent_observation
        else:
            super(AndroidDeviceEnv, self).render(mode=mode)  # just raise an exception for invalid mode

    def get_new_observation(self):
        """
        Gather the observation object from the observation buffer and decode the image into a numpy array that aligns with the observation space.
        """
        # Blocking read from the observation buffer.
        observation = self.observation_buffer.blocking_read_elem()

        # Decode image bytes into a numpy array.
        pil_image = Image.open(StringIO(observation.image_bytes))

        return np.array(pil_image)

    def compute_reward(self, new_observation):
        """
        Compute reward value based on the new observation image. It utilizes current state information like
        current observation, number of steps so far, and this new observation to compute the reward.

        Can be overridden to include more information from other state variables if necessary.

        :param new_observation: numpy array containing the new screen image (H x W x C) where C is the number of
        channels (C = 3 for RGB).
        :return: float reward value.
        """
        raise NotImplementedError
