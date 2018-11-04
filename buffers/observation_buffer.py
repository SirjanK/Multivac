from buffers.buffer import Buffer
from session.time_manager import TimeManager
from eventobjects.observation import Observation


class ObservationBuffer(Buffer):
    """
    The ObservationBuffer object maintains a queue of observations from a device.
    """
    IMAGE_TYPE = "jpg"

    def __init__(self):
        """
        Initializes the ObservationBuffer object.
        """
        super(ObservationBuffer, self).__init__()
        self.time_manager = TimeManager.get_default_instance()

    def enrich_element_to_queue(self, written_elem):
        """
        Enrich an element to add to the queue. Wrap into an Observation object.
        :param written_elem: element from the internal queue. MonkeyImage instance.
        :return: enriched Observation element.
        """
        timestamp = self.time_manager.timeit()

        # Convert MonkeyImage to string bytes. Format specified by IMAGE_TYPE.
        image_bytes = written_elem.convertToBytes(self.IMAGE_TYPE)

        return Observation(image_bytes, timestamp)
