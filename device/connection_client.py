from device.threads.action_thread import ActionThread
from device.threads.observation_thread import ObservationThread
import time
import redis
from com.android.monkeyrunner import MonkeyRunner


class ConnectionClient:
    """
    The ConnectionClient object manages I/O with a connected device via the monkeyrunner API.
    It maintains a two way interface between an ActionBuffer, ObservationBuffer pair and the device.
    """

    def __init__(self, redis_port, observation_delta):
        """
        Initialize the client. Verify connection with the device and setup the two buffers.
        :param redis_port: Port to either start or retrieve the redis connection.
        :param observation_delta: time interval in milliseconds that the client should poll for an
        image from the device.
        """
        connected_device = MonkeyRunner.waitForConnection()
        print("Device found!")

        # Start Redis connection on specified port.
        self.redis_connection = redis.Redis(port=redis_port)

        self.observation_thread = ObservationThread(self.redis_connection, connected_device, observation_delta)
        self.action_thread = ActionThread(self.redis_connection, connected_device)

    def stream_observations(self):
        """
        Start a new thread to stream observations to the observation buffer.
        """
        self.observation_thread.start()

    def start_action_input(self):
        """
        Start a new thread to listen to actions in the action buffer, and take action once an element is found.
        """
        self.action_thread.start()

    def wait(self, timeout):
        """
        Wait for the action and observation threads to terminate or until the timeout expiry is reached.
        :param timeout: time in seconds to wait.
        """
        time.sleep(timeout)
        self.shutdown()

    def shutdown(self):
        """
        Shutdowns the connection client.
        """
        self.redis_connection.shutdown()
        self.observation_thread.shutdown()
        self.action_thread.shutdown()
