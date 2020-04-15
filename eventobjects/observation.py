import pickle


class Observation(object):
    """
    Observation object that designates a response from the device.
    """

    def __init__(self, image_bytes):
        """
        Initializes the Observation object.
        :param image_bytes: string of png encoded image.
        """

        self.image_bytes = image_bytes

    def serialize(self):
        """
        Serialize the given observation object to a string. This involves serializing JUST the image bytes.
        :return: string representation of the observation.
        """

        return pickle.dumps(self.image_bytes, protocol=2)

    @staticmethod
    def deserialize(str_repr):
        """
        Deserialize the str_repr of an observation to an observation object.
        :param str_repr: String representation of an observation.
        :return: Observation object.
        """

        # Custom deserialization that involves wrapping the result into a new Observation object.
        img_bytes = pickle.loads(str_repr, encoding='bytes')

        return Observation(img_bytes)
