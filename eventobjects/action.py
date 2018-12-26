import pickle


class Action(object):
    """
    Action object that designates a click on the mobile screen at a certain time.
    """

    def __init__(self, click_coordinate, timestamp):
        """
        Initializes the Action object.
        :param click_coordinate: tuple of (x, y) coordinates on the screen.
        :param timestamp: float elapsed time in milliseconds from session start.
        """
        self.click_coordinate = click_coordinate
        self.timestamp = timestamp

    def serialize(self):
        """
        Serialize the given action object to a string.
        :return: string representation of the action.
        """
        return pickle.dumps(self, protocol=2)

    @staticmethod
    def deserialize(str_repr):
        """
        Deserialize the str_repr of an Action to an action object.
        :param str_repr: String representation of an action.
        :return: Action object.
        """
        return pickle.loads(str_repr)
