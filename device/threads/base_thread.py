from threading import Thread


class BaseThread(Thread):
    """
    Basic Thread object that is built on top of the default threading.Thread class. It provides a shutdown hook.
    """

    def __init__(self, redis_client, device):
        """
        Initializes the thread with the given device.
        :param redis_client: Active connection to the redis DB
        :param device: MonkeyDevice object of the connected device.
        """
        super(BaseThread, self).__init__()
        self.redis_client = redis_client
        self.device = device
        self.is_running = True

    def shutdown(self):
        """
        Mark the thread to be shutdown.
        """
        self.is_running = False
