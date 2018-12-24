from buffers.buffer import Buffer

ACTION_BUFFER_NAME = "action_buffer"


class ActionBuffer(Buffer):
    """
    The ActionBuffer class abstracts away the underlying redis list containing actions that should
    be taken on the device.
    """

    def __init__(self, redis_client):
        """
        Initialize the ObservationBuffer.
        :param redis_client: Redis client for an active connection.
        """
        super(ActionBuffer, self).__init__(ACTION_BUFFER_NAME, redis_client)
