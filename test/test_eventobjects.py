from eventobjects.action import Action
from eventobjects.observation import Observation


def test_action():
    """
    Simple tests for Action serialization and deserialization.
    """
    test_action_with_ground_truth((12, 20), 4214234)
    test_action_with_ground_truth((112, 2342342), 0)
    test_action_with_ground_truth((35532423, 345345345), 2991992)


def test_action_with_ground_truth(click_coordinate, timestamp):
    action = Action(click_coordinate, timestamp)
    assert type(action.click_coordinate) == tuple
    assert type(timestamp) == int

    action_str = action.serialize()
    assert type(action_str) == bytes

    action_prime = Action.deserialize(action_str)
    assert type(action_prime) == Action

    assert type(action_prime.click_coordinate) == tuple
    assert type(action_prime.timestamp) == int

    assert action_prime.click_coordinate == click_coordinate
    assert action_prime.timestamp == timestamp


def test_observation():
    """
    Simple tests for Observation serialization and deserialization.
    """
    test_observation_with_ground_truth(b'adfasfasfasfasf', 353535325)
    test_observation_with_ground_truth(b'', 0)
    test_observation_with_ground_truth(b'34324324324121jkjlkf23k4h24hlkl2k3h4lkh324lh24lkj2', 2222222)


def test_observation_with_ground_truth(image_bytes, timestamp):
    observation = Observation(image_bytes, timestamp)
    assert type(observation.image_bytes) == bytes
    assert type(timestamp) == int

    observation_str = observation.serialize()
    assert type(observation_str) == bytes

    observation_prime = Observation.deserialize(observation_str)
    assert type(observation_prime) == Observation

    assert type(observation_prime.image_bytes) == bytes
    assert type(observation_prime.timestamp) == int

    assert observation_prime.image_bytes == image_bytes
    assert observation_prime.timestamp == timestamp


if __name__ == '__main__':
    test_action()
    test_observation()
