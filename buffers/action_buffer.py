from buffers.buffer import Buffer
from device.time_manager import TimeManager
from eventobjects.action import Action


class ActionBuffer(Buffer):
    """
    The ActionBuffer object maintains a queue of actions that will be taken on a device.
    """

    def __init__(self):
        """
        Initializes the ActionBuffer object.
        """
        super(ActionBuffer, self).__init__()
        self.time_manager = TimeManager.get_default_instance()

    def enrich_element_from_queue(self, queue_elem):
        """
        Enrich an element to return to a client. Wrap into an Action object.
        :param queue_elem: element from the internal queue. Tuple of (x, y) coordinate.
        :return: enriched Action element.
        """
        timestamp = self.time_manager.timeit()
        return Action(queue_elem, timestamp)
