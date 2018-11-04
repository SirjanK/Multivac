import threading
import sys


class BaseThread(threading.Thread):
    """
    Basic Thread object that is built on top of the default threading.Thread class. It provides a shutdown hook.
    """

    @classmethod
    def shutdown(cls):
        """
        Shutdown the thread.
        """
        sys.exit()
