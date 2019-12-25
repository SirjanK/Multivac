"""
File that contains any environments that can be used.
"""

from environment.mean_pixel_difference_env import MeanPixelDifferenceEnv


def create_environment_instance_fn(cls):
    return lambda action_buffer, observation_buffer, image_height, image_width: \
        cls.__init__(action_buffer, observation_buffer, image_height, image_width)


# Dict mapping from environment name to a function that creates an instance of that environment.
ENVIRONMENTS = {
    'MeanPixelDifferenceEnv': create_environment_instance_fn(MeanPixelDifferenceEnv)
}
