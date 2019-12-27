import redis
import time

from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice

from buffers.action_buffer import ActionBuffer
from buffers.observation_buffer import ObservationBuffer
from eventobjects.observation import Observation


class ConnectionClient:
    """
    The ConnectionClient object manages I/O with a connected device via the monkeyrunner API.
    It maintains a two way interface between an ActionBuffer, ObservationBuffer pair and the device.

    Specifically, the manages listening for updates to the action buffer and taking action once
    an element arrives. It blocks otherwise. When the action is taken, it waits for a predefined amount of time
    before taking a screenshot of the device. This is then placed into the observation buffer.
    """

    # Time in seconds to wait to screenshot if a reset action is taken.
    REBOOT_TIME = 10

    def __init__(self, redis_port, observation_delta=1000):
        """
        Initialize the client. Verify connection with the device and setup the two buffers.
        :param redis_port: Port to either start or retrieve the redis connection.
        :param observation_delta: time interval in milliseconds that the client should poll for an
        image from the device.
        """
        print("Waiting for device connection.")
        self.connected_device = MonkeyRunner.waitForConnection()
        print("Device found!")

        # Start Redis connection on specified port.
        self.redis_client = redis.Redis(port=redis_port)

        # Initialize buffers.
        self.action_buffer = ActionBuffer(self.redis_client)
        self.observation_buffer = ObservationBuffer(self.redis_client)

        self.observation_delta = observation_delta / 1000.0

    def start(self):
        """
        Starts an infinite cycle of listening to the action buffer and populating the observation buffer.
        Once terminated, the shutdown function will be invoked.

        Reads action from the action_buffer and applies it to the device. Then waits observation_delta milliseconds
        and takes a screenshot of the device.
        """
        while True:
            action = self.action_buffer.blocking_read_elem()
            self.take_action(action)

            time.sleep(self.observation_delta)

            self.gather_observation()

    def take_action(self, action):
        """
        Takes the given action on the device.
        :param action: Action object.
        """
        if action.is_reset_action:
            # Reboot device if the action specified is 'reset'
            self.connected_device.reboot("None")

            print("Action taken! This is a reset action causing device reboot")

            # Custom sleep for a longer period of time since reboot may take a while
            time.sleep(self.REBOOT_TIME)

            # Reconnect device
            self.connected_device = MonkeyRunner.waitForConnection()
        else:
            x, y = action.click_coordinate
            self.connected_device.touch(x, y, MonkeyDevice.DOWN_AND_UP)
            print("Action taken! Coordinates (" + str(x) + "," + str(y) + ")")

    def gather_observation(self):
        """
        Take a screenshot of the device and add the image bytes (png format) into the observation buffer.
        """
        device_image = self.connected_device.takeSnapshot()

        observation = Observation(device_image.convertToBytes("png"))
        self.observation_buffer.put_elem(observation)

        print("Image added to the observation buffer")

    def shutdown(self):
        """
        Shutdowns the connection client.
        """
        self.redis_client.shutdown()
