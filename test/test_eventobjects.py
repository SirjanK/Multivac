from eventobjects.action import Action
from eventobjects.observation import Observation


def test_action():
    """
    Simple tests for Action serialization and deserialization.
    """
    test_action_with_ground_truth((12, 20))
    test_action_with_ground_truth((112, 2342342))
    test_action_with_ground_truth((35532423, 345345345))


def test_action_with_ground_truth(click_coordinate):
    action = Action(click_coordinate)
    assert type(action.click_coordinate) == tuple

    action_str = action.serialize()
    assert type(action_str) == bytes

    action_prime = Action.deserialize(action_str)
    assert type(action_prime) == Action

    assert type(action_prime.click_coordinate) == tuple

    assert action_prime.click_coordinate == click_coordinate


def test_observation():
    """
    Simple tests for Observation serialization and deserialization.
    """
    test_observation_with_ground_truth(b'adfasfasfasfasf')
    test_observation_with_ground_truth(b'')
    test_observation_with_ground_truth(b'34324324324121jkjlkf23k4h24hlkl2k3h4lkh324lh24lkj2')


def test_observation_with_ground_truth(image_bytes):
    observation = Observation(image_bytes)
    assert type(observation.image_bytes) == bytes

    observation_str = observation.serialize()
    assert type(observation_str) == bytes

    observation_prime = Observation.deserialize(observation_str)
    assert type(observation_prime) == Observation

    assert type(observation_prime.image_bytes) == bytes

    assert observation_prime.image_bytes == image_bytes


if __name__ == '__main__':
    test_action()
    print("Test action succeeded.")
    test_observation()
    print("Test observation succeeded.")
