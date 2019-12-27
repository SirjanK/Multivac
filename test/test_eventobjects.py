from eventobjects.action import Action
from eventobjects.observation import Observation


def test_action():
    helper_test_action_with_ground_truth((12, 20))
    helper_test_action_with_ground_truth((112, 2342342))
    helper_test_action_with_ground_truth((35532423, 345345345))


def test_observation():
    helper_test_observation_with_ground_truth("adfasfasfasfasf")
    helper_test_observation_with_ground_truth("")
    helper_test_observation_with_ground_truth("34324324324121jkjlkf23k4h24hlkl2k3h4lkh324lh24lkj2")


def helper_test_action_with_ground_truth(click_coordinate):
    action = Action(click_coordinate)
    assert type(action.click_coordinate) == tuple

    action_str = action.serialize()
    assert type(action_str) == bytes

    action_prime = Action.deserialize(action_str)
    assert type(action_prime) == Action

    assert type(action_prime.click_coordinate) == tuple

    assert action_prime.click_coordinate == click_coordinate


def helper_test_observation_with_ground_truth(image_bytes):
    observation = Observation(image_bytes)
    assert type(observation.image_bytes) == str

    observation_str = observation.serialize()
    assert type(observation_str) == bytes

    observation_prime = Observation.deserialize(observation_str)
    assert type(observation_prime) == Observation

    assert type(observation_prime.image_bytes) == str

    assert observation_prime.image_bytes == image_bytes
