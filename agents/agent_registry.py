"""
File that contains any agents that can be used.

TODO: Add way to parametrize these agents
"""

from agents.stable_baseline_agents import *
from agents.continuous_random_agent import ContinuousRandomAgent


# Dictionary mapping from environment to an agent for that environment
AGENTS = {
    'ppo2': lambda env: PPO2Agent(env),
    'ddpg': lambda env: DDPGAgent(env),
    'random': lambda env: ContinuousRandomAgent(env)
}
