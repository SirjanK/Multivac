import time

from threading import Thread

from eventobjects.action import Action
from eventobjects.observation import Observation

from buffers.action_buffer import ActionBuffer
from buffers.observation_buffer import ObservationBuffer


class DeviceThread(Thread):
    """
    The DeviceTHread manages listening for updates to the action buffer and taking action once
    an element arrives. It blocks otherwise. When the action is taken, it waits for a predefined amount of time
    before taking a screenshot of the device. This is then placed into the observation buffer.
    """

    # Time in seconds to wait to screenshot if a reset action is taken.
    REBOOT_TIME = 10

    def __init__(self, redis_client, device, observation_delta=1000):
        """
        Initializes the thread with the given device.
        :param redis_client: Active connection to the redis DB
        :param device: MonkeyDevice object of the connected device.
        :param observation_delta: Time in milliseconds to wait after taking the action to screenshot an observation.
        """
        super(BaseThread, self).__init__()

        # Initialize buffers.
        self.action_buffer = ActionBuffer(redis_client)
        self.observation_buffer = ObservationBuffer(redis_client)

        self.device = device

        self.observation_delta = observation_delta / 1000.0

        self.is_running = True

    def run(self):
        """
        Executable for the thread.

        Reads action from the action_buffer and applies it to the device. Then waits observation_delta milliseconds
        and takes a screenshot of the device.
        """
        while self.is_running:
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
            # TODO: figure out if there's a better way to do this instead of rebooting.
            # Reboot device if the action specified is 'reset'
            self.device.reboot("None")

            print("Action taken! This is a reset action causing device reboot")

            # Custom sleep for a longer period of time since reboot may take a while
            time.sleep(REBOOT_TIME)
        else:
            x, y = action.click_coordinate
            self.device.touch(x, y, MonkeyDevice.DOWN_AND_UP)
            print("Action taken! Coordinates (" + str(x) + "," + str(y) + ")")

    def gather_observation(self, observation):
        """
        Take a screenshot of the device and add the image bytes (png format) into the observation buffer.
        """
        device_image = self.device.takeSnapshot()

        observation = Observation(device_image.convertToBytes("png"))
        self.observation_buffer.put_elem(observation)

        print("Image added to observation buffer")

    def shutdown(self):
        """
        Mark the thread to be shutdown.
        """
        self.is_running = False
