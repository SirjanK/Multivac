import time


class TimeManager(object):
    """
    The TimeManager class provides a static interface to provide system level timing information.
    It gathers elapsed time from when a session begins.

    This object should not be instantiated manually. Instead the get_default_instance() function should be called
    on a per-session basis.
    """

    _instance = None

    def __init__(self):
        """
        Initializes the TimeManager. Should not be instantiated directly outside of the get_default_instance()
        function.
        """
        # Set start_time to None until explicitly started.
        self.start_time = None

    def start(self):
        """
        Start the time manager.
        """
        self.start_time = time.time()

    def timeit(self):
        """
        Calculates the elapsed time since start_time.
        :return: current time minus the start time.
        """
        if self.start_time:
            return time.time() - self.start_time
        else:
            raise Exception("Time Manager was never started.")

    @classmethod
    def get_default_instance(cls):
        """
        Get an instance of the time manager if it exists. Otherwise, initialize one.
        :return: TimeManager object.
        """
        if not cls._instance:
            cls._instance = TimeManager()

        return cls._instance
