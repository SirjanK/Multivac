import abc
from queue import LifoQueue


class Buffer(abc.ABC):
    """
    The Buffer class defines a clean interface to read and write from a two-way buffer.
    """

    def __init__(self):
        """
        Initializes the buffer object with its own internal queue.
        """
        self.queue = LifoQueue()

    def read(self):
        """
        Read the oldest element from the Buffer if available. If not available, block until an element is available.
        :return: Element from the Buffer.
        """
        element = self.queue.get(block=True)
        return self.enrich_element(element)

    def write(self, element):
        """
        Writes to the Buffer.
        :param element: element to write to the end of the Buffer.
        """
        self.queue.put(element)

    @abc.abstractmethod
    def enrich_element(self, queue_elem):
        """
        Enrich an element to return to a client.
        :param queue_elem: element from the internal queue.
        :return: enriched element.
        """
        raise NotImplementedError()
