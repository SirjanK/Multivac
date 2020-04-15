import logging
import redis
import time

from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
from com.android.ddmlib import TimeoutException

from buffers.action_buffer import ActionBuffer
from buffers.observation_buffer import ObservationBuffer
from device.adb_shell_cmds_manager import AdbShellCmdsManager
from eventobjects.observation import Observation


class ConnectionClient:
    """
    The ConnectionClient object manages I/O with a connected device via the monkeyrunner API.
    It maintains a two way interface between an ActionBuffer, ObservationBuffer pair and the device.

    Specifically, the client manages listening for updates to the action buffer and taking action once
    an element arrives. It blocks otherwise. When the action is taken, it waits for a predefined amount of time
    before taking a screenshot of the device. This is then placed into the observation buffer.
    """

    # Time in seconds to wait to screenshot if a reset action is taken.
    RESET_TIME = 5

    # Max number of times to retry taking device screenshot
    MAX_SCREENSHOT_RETRY = 3

    def __init__(self, redis_port, observation_delta=250):
        """
        Initialize the client. Verify connection with the device and setup the two buffers.
        :param redis_port: Port to start the redis connection.
        :param observation_delta: Time interval in milliseconds that the client should poll for an
        image from the device.
        """

        self.logger = logging.getLogger("ConnectionClient")
        self.logger.addHandler(logging.StreamHandler())
        self.logger.setLevel(logging.DEBUG)

        self.logger.info("Waiting for device connection.")
        self.connected_device = MonkeyRunner.waitForConnection()
        self.logger.info("Device found!")

        # Start Redis connection on specified port.
        self.redis_client = redis.Redis(port=redis_port)

        # Initialize buffers.
        self.action_buffer = ActionBuffer(self.redis_client)
        self.observation_buffer = ObservationBuffer(self.redis_client)

        self.observation_delta = observation_delta / 1000.0

        self.adb_shell_cmds_manager = AdbShellCmdsManager(self.connected_device)

    def start(self):
        """
        First, send a screenshot message to the observation buffer to provide an example image response. Then,
        start an infinite cycle of listening to the action buffer and populating the observation buffer.
        Once terminated, the shutdown function will be invoked.

        In each iteration, read action from the action_buffer and apply it to the device. Then wait observation_delta
        milliseconds and take a screenshot of the device.
        """

        try:
            # Initial step is to pass a screenshot into the observation buffer
            self.logger.debug("Sending inital observation image")
            self.gather_observation()

            while True:
                action = self.action_buffer.blocking_read_elem()
                self.take_action(action)

                time.sleep(self.observation_delta)

                self.gather_observation()
        except redis.connection.ConnectionError:
            self.redis_client.shutdown()
            self.logger.info("Redis has been terminated, connection client is shut down.")

    def take_action(self, action):
        """
        Takes the given action on the device.
        :param action: Action object.
        """

        if action.is_reset_action:
            # Reset device to its original state by closing all active applications.
            self.adb_shell_cmds_manager.close_applications()

            self.logger.debug("Action taken! This is a reset action closing all open applications")

            # Custom sleep for a longer period of time since reboot may take a while
            time.sleep(self.RESET_TIME)
        else:
            x, y = action.click_coordinate
            device_x, device_y = int(x), int(y)
            self.connected_device.touch(device_x, device_y, MonkeyDevice.DOWN_AND_UP)
            self.logger.debug("Action taken! Coordinates (" + str(device_x) + "," + str(device_y) + ")")

    def gather_observation(self):
        """
        Take a screenshot of the device and add the image bytes (png format) into the observation buffer.
        """

        num_retry = 0
        while num_retry < self.MAX_SCREENSHOT_RETRY:
            try:
                device_image = self.connected_device.takeSnapshot()

                img_bytes = device_image.convertToBytes().tostring()

                observation = Observation(img_bytes)

                self.observation_buffer.put_elem(observation)

                return
            except TimeoutException:
                self.logger.error("Taking screenshot failed. Trying again.")
                num_retry += 1

        self.logger.critical("Taking screenshot failed after max retries. Failing out.")
        raise Exception("Taking screenshot failed.")

    def shutdown(self):
        """
        Shutdown the connection client.
        """

        self.logger.info("Connection client shutting down.")

        # Kill any monkey processes running on the device. This is required due to a bug in monkeyrunner itself
        self.adb_shell_cmds_manager.shutdown_monkey_on_device()
