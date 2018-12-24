from device.threads.base_thread import BaseThread
from device.time_manager import TimeManager
from eventobjects.observation import Observation
from buffers.observation_buffer import ObservationBuffer
import time


class ObservationThread(BaseThread):
    """
    The ObservationThread manages streaming observations from the device into the observation buffer.
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

        while self.is_running:
            device_image = self.device.takeSnapshot()

            print("Trying to write image")
            # TODO implement write to disk without blocking thread.
            device_image.writeToFile("./out/" + str(image_no) + ".png", "png")

            # TODO implement write to observation buffer.
            log_str = "Observation event: Image " + str(image_no) + " at timestamp " \
                      + str(TimeManager.get_default_instance().timeit())
            print(log_str)
            observation = Observation(device_image.convertToBytes("png"), TimeManager.get_default_instance().timeit())
            self.observation_buffer.put_elem(observation)

            time.sleep(self.observation_delta / 1000.0)
            image_no += 1
