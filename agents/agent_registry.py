"""
File that contains any agents that can be used.

TODO: Add way to parametrize these agents
"""

from agents.continuous_random_agent import ContinuousRandomAgent


# Dictionary mapping from environment to an agent for that environment
AGENTS = {
    'random': lambda env: ContinuousRandomAgent(env)
}
