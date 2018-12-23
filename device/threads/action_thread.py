from device.threads.base_thread import BaseThread
from device.connection_client import ACTION_BUFFER
from com.android.monkeyrunner import MonkeyDevice


class ActionThread(BaseThread):
    """
    The ActionThread manages listening for updates to the action_buffer and taking action once
    an element arrives. It blocks otherwise.
    """

    def run(self):
        """
        Executable for the thread.

        Reads action from the action_buffer and applies it to the device.
        """
        while self.is_running:
            # random_coordinates = (randint(0, 200), randint(0, 200))
            # action = Action(random_coordinates, TimeManager.get_default_instance().timeit())
            action = self.redis_connection.blpop(ACTION_BUFFER)
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
