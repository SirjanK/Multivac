import redis
import time

from buffers.action_buffer import ActionBuffer
from buffers.observation_buffer import ObservationBuffer
from eventobjects.action import Action
from eventobjects.observation import Observation


def test_action_buffer():
    redis_client = redis.Redis()

    action_buffer = ActionBuffer(redis_client)

    action_buffer.put_elem(Action((40, 10)))
    action_buffer.put_elem(Action((10, 70)))
    action_buffer.put_elem(Action((90, 10)))

    assert(action_buffer.read_elem().click_coordinate == (90, 10))

    action_buffer.put_elem(Action((2, 4)))

    assert(action_buffer.read_elem().click_coordinate == (2, 4))
    assert(action_buffer.read_elem().click_coordinate == (10, 70))
    assert(action_buffer.read_elem().click_coordinate == (40, 10))

    redis_client.shutdown()
    time.sleep(1)  # Allow time for the redis client to shut down


def test_observation_buffer():
    redis_client = redis.Redis()

    obs_buffer = ObservationBuffer(redis_client)

    obs_buffer.put_elem(Observation("img1"))
    obs_buffer.put_elem(Observation("img2"))

    assert(obs_buffer.read_elem().image_bytes == "img2")

    obs_buffer.put_elem(Observation("img3"))

    assert(obs_buffer.read_elem().image_bytes == "img3")
    assert(obs_buffer.read_elem().image_bytes == "img1")

    redis_client.shutdown()
    time.sleep(1)  # Allow time for the redis client to shut down
