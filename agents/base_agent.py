from abc import ABC

from environment.android_device_env import AndroidDeviceEnv


class BaseAndroidAgent(ABC):
    """
    Base agent that provides a very simple interface: take in an environment that is an instance
    of AndroidDeviceEnv, and provide a `train()` and `predict()` function.
    """

    def __init__(self, env):
        """
        Initialize the agent.
        :param env: AndroidDeviceEnv instance this agent will act on.
        """
        assert(
            isinstance(env, AndroidDeviceEnv),
            'Agent must be initialized with an environment that is an instance of AndroidDeviceEnv.'
        )

        self.env = env

    def train(self, num_steps):
        """
        Train the agent.
        :param num_steps: number of steps to train.
        """
        raise NotImplementedError

    def predict(self, obs):
        """
        Predict next action to take on the environment.
        :param obs: observation image.
        :return: action instance (Box)
        """
        raise NotImplementedError
