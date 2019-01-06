class Buffer(object):
    """
    The Buffer class abstracts away the underlying redis list containing elements.
    """

    def __init__(self, buffer_name, redis_client):
        """
        Initialize the Buffer.
        :param buffer_name: Name of the redis list containing the buffer.
        :param redis_client: Redis client for an active connection.
        """
        self.buffer_name = buffer_name
        self.redis_client = redis_client

    def read_elem(self):
        """
        Read elem from the redis list.
        :return: elem.
        """
        read_str = self.redis_client.lpop(self.buffer_name)
        return self.deserialize_elem(read_str)

    def blocking_read_elem(self):
        """
        Blocking read from the redis list.
        :return: elem.
        """
        _, read_str = self.redis_client.blpop(self.buffer_name)
        return self.deserialize_elem(read_str)

    def put_elem(self, elem):
        """
        Places elem into the Buffer.
        :param elem: element to be placed at the end.
        """
        serialized_elem = self.serialize_elem(elem)
        self.redis_client.lpush(self.buffer_name, serialized_elem)

    def serialize_elem(self, elem):
        """
        Serialize the buffer elem to a string.
        :param elem: buffer element.
        :return: String representation of elem.
        """
        raise NotImplementedError()

    def deserialize_elem(self, elem_str):
        """
        Deserialize the string representation of a buffer element.
        :param elem_str: String representation of a buffer element.
        :return: buffer element.
        """
        raise NotImplementedError()
