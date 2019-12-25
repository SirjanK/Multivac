from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import PPO2, DDPG

from agents.base_agent import BaseAndroidAgent


class PPO2Agent(BaseAndroidAgent):
    """
    Uses the PPO2 algorithm as the agent.
    """

    def __init__(self, env):
        super(PPO2Agent, self).__init__(env)

        self.model = PPO2(MlpPolicy, DummyVecEnv(lambda: env))

    def train(self, num_steps):
        self.model.learn(total_timesteps=num_steps)

    def predict(self, obs):
        action, _ = self.model.predict(obs)
        return action


class DDPGAgent(BaseAndroidAgent):
    """
    Uses the DDPG algorithm as the agent.
    """

    def __init__(self, env):
        super(DDPGAgent, self).__init__(env)

        self.model = DDPG(MlpPolicy, DummyVecEnv(lambda: env))

    def train(self, num_steps):
        self.model.learn(total_timesteps=num_steps)

    def predict(self, obs):
        action, _ = self.model.predict(obs)
        return action
