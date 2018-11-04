class Action:
    """
    Action object that designates a click on the mobile screen at a certain time.
    """

    def __init__(self, click_coordinate, timestamp):
        """
        Initializes the Action object.
        :param click_coordinate: tuple of (x, y) coordinates on the screen.
        :param timestamp: float elapsed time in milliseconds from session start.
        """
        assert(type(click_coordinate) == tuple, "Invalid type for click_coordinate.")
        assert(type(timestamp) == float, "Invalid type for timestamp.")
        assert(len(click_coordinate) == 2, "Invalid number of coordinates.")
        assert(type(click_coordinate[0]) == float and type(click_coordinate[1]) == float, "Invalid type of coordinate.")

        self.click_coordinates = click_coordinate
        self.timestamp = timestamp
