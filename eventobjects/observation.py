class Observation:
    """
    Observation object that designates a response image of the mobile screen at a certain time.
    """

    def __init__(self, image_bytes, timestamp):
        """
        Initializes the Observation object.
        :param image_bytes: string of jpg encoded image.
        :param timestamp: float elapsed time in milliseconds from session start.
        """
        assert(type(image_bytes) == str, "Invalid type for image_bytes.")
        assert(type(timestamp) == float, "Invalid type for timestamp.")

        self.image_bytes = image_bytes
        self.timestamp = timestamp
