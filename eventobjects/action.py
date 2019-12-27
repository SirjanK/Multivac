import pickle


class Action(object):
    """
    Action object that designates a click on the mobile screen.
    """

    def __init__(self, click_coordinate, is_reset_action=False):
        """
        Initializes the Action object.
        :param click_coordinate: tuple of (x, y) coordinates on the screen.
        :param is_reset_action: flag to indicate whether this action is a 'reset' action
        (return device to initial state)
        """

        self.click_coordinate = click_coordinate
        self.is_reset_action = is_reset_action

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


# Singleton instance of the Action object denoting a 'reset' action.
RESET_ACTION = Action(None, is_reset_action=True)
