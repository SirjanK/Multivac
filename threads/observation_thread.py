from threads.base_thread import BaseThread
from buffers.buffer import Buffer


class ObservationThread(BaseThread):
    """
    The ObservationThread manages streaming observations from the device into the observation buffer.
    """

    def __init__(self, observation_buffer, observation_delta):
        """
        Initialize the ObservationThread.
        :param observation_buffer: buffer to which observations should be placed.
        :param observation_delta: time interval to poll the device for observations.
        """
        super(ObservationThread, self).__init__()
        assert(isinstance(observation_buffer, Buffer), "Invalid type for the observation_buffer.")
        assert(type(observation_delta) == float, "Invalid type for the observation_delta.")
        self.observation_buffer = observation_buffer
        self.observation_delta = observation_delta

    def run(self):
        """
        Executable for the thread.
        """
        # TODO: implement
        pass
