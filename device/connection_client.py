from device.device_thread import DeviceThread
import time
import redis
from com.android.monkeyrunner import MonkeyRunner


class ConnectionClient:
    """
    The ConnectionClient object manages I/O with a connected device via the monkeyrunner API.
    It maintains a two way interface between an ActionBuffer, ObservationBuffer pair and the device.

    Specifically, it maintains another thread (DeviceThread) that continually takes actions and gathers observations.
    """

    def __init__(self, redis_port, observation_delta):
        """
        Initialize the client. Verify connection with the device and setup the DeviceThread.
        :param redis_port: Port to either start or retrieve the redis connection.
        :param observation_delta: time interval in milliseconds that the client should poll for an
        image from the device.
        """
        connected_device = MonkeyRunner.waitForConnection()
        print("Device found!")

        # Start Redis connection on specified port.
        self.redis_client = redis.Redis(port=redis_port)

        self.device_thread = DeviceThread(self.redis_client, connected_device, observation_delta)

    def start(self):
        """
        Starts new thread to listen to actions in the action buffer, take action once an element is found, and gather observations.
        """
        self.device_thread.start()

    def shutdown(self):
        """
        Shutdowns the connection client.
        """
        self.device_thread.shutdown()
        self.redis_client.shutdown()
