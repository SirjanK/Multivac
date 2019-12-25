from device.threads.base_thread import BaseThread
from eventobjects.observation import Observation
from buffers.observation_buffer import ObservationBuffer


class ObservationThread(BaseThread):
    """
    The ObservationThread manages placing observations from the device into the observation buffer once
    """

    def __init__(self, redis_client, device, observation_delta):
        """
        Initialize the ObservationThread.
        :param redis_client: Active connection to the redis DB
        :param device: MonkeyDevice object of the connected device.
        :param observation_delta: time interval to poll the device for observations. (milliseconds)
        """
        super(ObservationThread, self).__init__(redis_client, device)
        self.observation_delta = observation_delta
        self.observation_buffer = ObservationBuffer(redis_client)

    def run(self):
        """
        Executable for the thread.

        Takes a snapshot of the device screen every observation_delta milliseconds and places it in the
        observation buffer as well as writing the image to disk.
        """
        image_no = 0
        sleep_time = self.observation_delta / 1000.0

        while self.is_running:
            device_image = self.device.takeSnapshot()

            print("Trying to write image")
            # TODO implement write to disk without blocking thread.
            device_image.writeToFile("./out/" + str(image_no) + ".png", "png")

            observation = Observation(device_image.convertToBytes("png"))
            self.observation_buffer.put_elem(observation)

            time.sleep(sleep_time)
            image_no += 1
