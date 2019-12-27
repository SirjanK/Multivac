import numpy as np

from environment.mean_pixel_difference_env import MeanPixelDifferenceEnv


def test_mean_pixel_difference_reward():
    env = MeanPixelDifferenceEnv(None, None, 100, 50)

    env.most_recent_observation = np.zeros(shape=(100, 50, 3))

    new_obs = np.ones(shape=(100, 50, 3))
    reward = env.compute_reward(new_obs)

    assert(reward == 1)

    env.most_recent_observation = new_obs

    new_obs = np.array([
        3 * np.ones(shape=(100, 50)),
        42 * np.ones(shape=(100, 50)),
        30 * np.ones(shape=(100, 50))
    ]).transpose([1, 2, 0])

    reward = env.compute_reward(new_obs)

    assert(reward == 24)
