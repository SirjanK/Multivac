import numpy as np

from agents.base_agent import BaseAndroidAgent


class ContinuousRandomAgent(BaseAndroidAgent):
    """
    The random agent simply chooses coordinates uniformly at random from continuous action space.
    """

    def __init__(self, env):
        super(ContinuousRandomAgent, self).__init__(env)

        low, high = env.action_space.low, env.action_space.high

        # Function that returns a coordinate each time it is called.
        self.random_coordinate_generator = lambda: [np.random.uniform(low[i], high[i]) for i in range(len(low))]

    def take_action(self, _):
        # Regardless of the observation, predict a random action
        return self.random_coordinate_generator()
