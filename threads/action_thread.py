from threads.base_thread import BaseThread
from buffers.buffer import Buffer


class ActionThread(BaseThread):
    """
    The ActionThread manages listening for updates to the action_buffer and taking action once
    an element arrives. It blocks otherwise.
    """

    def __init__(self, action_buffer):
        """
        Initializes the ActionThread.
        :param action_buffer: buffer from which actions should be read.
        """
        super(ActionThread, self).__init__()
        assert(isinstance(action_buffer, Buffer), "Invalid type for the action_buffer.")
        self.action_buffer = action_buffer

    def run(self):
        """
        Executable for the thread.
        """
        # TODO: implement
        pass
