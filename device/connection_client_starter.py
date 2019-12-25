"""
This is a starter script for the connection_client. It requires the following cmd line arguments in order:
  i) redispy path: local path to redispy library
  ii) port that redis server is running
  iii) observation delta: time in milliseconds after an action is taken to take a screenshot of the device.
It is best to call this using `session_starter.py`.
"""


import atexit
import sys

from device.connection_client import ConnectionClient


if __name__ == '__main__':
    assert(len(sys.argv) == 4, 'Three arguments required.')

    redispy_path, redis_port, observation_delta = sys.argv[1:]

    # Append path to redispy lib
    # TODO cleaner solution than this for jython compatibility.
    sys.path.append(redispy_path)

    # Initialize the connection client.
    client = ConnectionClient(redis_port, observation_delta)

    atexit.register(lambda: client.shutdown())

    client.start()
