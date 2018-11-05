from buffers.buffer import Buffer
from threads.observation_thread import ObservationThread
from threads.action_thread import ActionThread


class ConnectionClient:
    """
    The ConnectionClient object manages I/O with a connected device via the monkeyrunner API.
    It maintains a two way interface between an ActionBuffer, ObservationBuffer pair and the device.
    """

    def __init__(self, action_buffer, observation_buffer, observation_delta):
        """
        Initialize the client. Verify connection with the device and setup the two buffers.
        :param action_buffer: action buffer the client uses.
        :param observation_buffer: observation buffer the client uses.
        :param observation_delta: float time interval in seconds that the client should poll for an
        image from the device.
        """
        assert(isinstance(action_buffer, Buffer), "Invalid type for the action_buffer.")
        assert(isinstance(observation_buffer, Buffer), "Invalid type for the observation_buffer.")
        assert(type(observation_delta) == float, "Invalid type for the observation_delta.")
        self.action_buffer = action_buffer
        self.observation_buffer = observation_buffer
        self.observation_thread = ObservationThread(self.observation_buffer, observation_delta)
        self.action_thread = ActionThread(self.action_buffer)

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

    def shutdown(self):
        """
        Shutdowns the connection client.
        """
        self.observation_thread.shutdown()
        self.action_thread.shutdown()
