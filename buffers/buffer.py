from queue import LifoQueue


class Buffer:
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
        :return: Enriched element from the Buffer.
        """
        element = self.queue.get(block=True)
        return self.enrich_element_from_queue(element)

    def write(self, element):
        """
        Writes the element after enriching to the Buffer.
        :param element: element to write to the end of the Buffer.
        """
        self.queue.put(self.enrich_element_to_queue(element))

    def enrich_element_from_queue(self, queue_elem):
        """
        Enrich an element to return to a client from the queue.
        By default, return the element without any enriching.
        :param queue_elem: element from the internal queue.
        :return: enriched element.
        """
        return queue_elem

    def enrich_element_to_queue(self, written_elem):
        """
        Enrich an element to add to the queue.
        By default, return the element without any enriching.
        :param written_elem: raw element client writes to the buffer.
        :return: enriched element to add to the queue.
        """
        return written_elem
