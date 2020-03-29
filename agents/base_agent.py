from abc import ABC

from environment.android_device_env import AndroidDeviceEnv


class BaseAndroidAgent(ABC):
    """
    Base agent that provides a very simple interface: take in an environment that is an instance
    of AndroidDeviceEnv, and provide a `take_action()` function.
    """

    def __init__(self, env):
        """
        Initialize the agent.
        :param env: AndroidDeviceEnv instance this agent will act on.
        """

        assert isinstance(env, AndroidDeviceEnv), \
            'Agent must be initialized with an environment that is an instance of AndroidDeviceEnv.'

        self.env = env

    def take_action(self, obs):
        """
        Predict next action to take on the environment.
        :param obs: observation image.
        :return: action instance (Box)
        """

        raise NotImplementedError
