import pickle


class Buffer:
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
        read_bytes = self.redis_client.lpop(self.buffer_name)
        return pickle.loads(read_bytes)

    def blocking_read_elem(self):
        """
        Blocking read from the redis list.
        :return: elem.
        """
        read_bytes = self.redis_client.blpop(self.buffer_name)
        return pickle.loads(read_bytes)

    def put_elem(self, elem):
        """
        Places elem into the Buffer.
        :param elem: element to be placed at the end.
        """
        pickled_elem = pickle.dumps(elem)
        self.redis_client.lpush(self.buffer_name, pickled_elem)
