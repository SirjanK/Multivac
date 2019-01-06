from buffers.action_buffer import ActionBuffer
from eventobjects.action import Action
from device.time_manager import TimeManager
from threading import Thread
from random import randint
import time
import os
import redis

# Redis related objects.
redis_client = redis.Redis(port=6379)
action_buffer = ActionBuffer(redis_client)


def test_connection_client_simple():
    """
    Tests the ConnectionClient implementation by launching a session with random input
    and validating that the appropriate number of actions and observations were taken.
    """
    print("Test ConnectionClient simple.")

    # Launch a thread to place an action in the ActionBuffer every 1 second.
    action_thread = Thread(target=place_random_actions, args=(1, 50))
    action_thread.start()

    # Run the connection_client.
    # TODO: Parameter parsing to get monkerunner path
    monkeyrunner_cmd = "~/Android/Sdk/tools/bin/monkeyrunner"
    os.system(monkeyrunner_cmd + " " + "device/connection_client_starter.py")

    action_thread.join()


def place_random_actions(interval, num_actions):
    """
    Places random actions to the ActionBuffer every interval seconds.
    :param interval: time between each action.
    :param num_actions: Total number of actions to place in the ActionBuffer
    """
    # TODO: Fix inconsistency between time managers.
    TimeManager.get_default_instance().start()

    # Give some time for the connection client to get started
    time.sleep(10)

    print("Starting to place actions into redis.")

    for _ in range(num_actions):
        time.sleep(interval)
        random_coordinates = (randint(0, 500), randint(0, 500))
        action = Action(random_coordinates, TimeManager.get_default_instance().timeit())
        action_buffer.put_elem(action)


if __name__ == '__main__':
    test_connection_client_simple()
