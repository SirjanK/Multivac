from buffers.buffer import Buffer
from eventobjects.observation import Observation

OBSERVATION_BUFFER_NAME = "observation_buffer"


class ObservationBuffer(Buffer):
    """
    The ObservationBuffer class abstracts away the underlying redis list containing observations that should
    be taken on the device.
    """

    def __init__(self, redis_client):
        """
        Initialize the ObservationBuffer.
        :param redis_client: Redis client for an active connection.
        """

        super(ObservationBuffer, self).__init__(OBSERVATION_BUFFER_NAME, redis_client)

    def serialize_elem(self, elem):
        return elem.serialize()

    def deserialize_elem(self, elem_str):
        return Observation.deserialize(elem_str)
