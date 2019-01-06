from device.threads.base_thread import BaseThread
from buffers.action_buffer import ActionBuffer
from com.android.monkeyrunner import MonkeyDevice


class ActionThread(BaseThread):
    """
    The ActionThread manages listening for updates to the action_buffer and taking action once
    an element arrives. It blocks otherwise.
    """

    def __init__(self, redis_client, device):
        """
        Initializes the ActionThread.

        :param redis_client: Active connection to the redis DB
        :param device: MonkeyDevice object of the connected device.
        """
        super(ActionThread, self).__init__(redis_client, device)
        self.action_buffer = ActionBuffer(redis_client)

    def run(self):
        """
        Executable for the thread.

        Reads action from the action_buffer and applies it to the device.
        """
        while self.is_running:
            action = self.action_buffer.blocking_read_elem()
            self.take_action(action)

    def take_action(self, action):
        """
        Takes the given action on the device.
        :param action: Action object.
        """
        x, y = action.click_coordinate
        self.device.touch(x, y, MonkeyDevice.DOWN_AND_UP)
        # TODO log action.
        print("Action taken! Coordinates (" + str(x) + "," + str(y) + ")")
