import numpy as np

from environment.android_device_env import AndroidDeviceEnv


class MeanPixelDifferenceEnv(AndroidDeviceEnv):
    def compute_reward(self, new_observation):
        """
        Computes the average pixel difference between the current and new observations.
        Agent learns to click on the screen so that there are visual changes going on.

        :param new_observation: numpy array containing the new screen image (H x W x C) where C is the number of
        channels (C = 3 for RGB).
        :return: float reward value.
        """

        image_diff = np.absolute(new_observation - self.most_recent_observation)

        return np.mean(image_diff)
