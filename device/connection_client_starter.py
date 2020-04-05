"""
This is a starter script for the connection_client. It requires the following cmd line arguments in order:
  i) redispy path: local path to redispy library
  ii) port that redis server is running
  iii) observation delta: time in milliseconds after an action is taken to take a screenshot of the device.
It is best to call this using `session_starter.py`.
"""

import os
import signal
import sys

assert(len(sys.argv) == 4, 'Three arguments required.')
redispy_path, redis_port, observation_delta = sys.argv[1:]

# Add the redispy (python 2.5 compatible version) library.
sys.path.append(redispy_path)

# This is to ensure jython will have the current project in its path.
sys.path.append(os.getcwd())

from device.connection_client import ConnectionClient

# Initialize the connection client.
client = ConnectionClient(int(redis_port), int(observation_delta))


def terminate_on_signal(signum, _):
    client.shutdown()

    # Graceful exit on sigterm since this is sent from parent process.
    if signum == signal.SIGTERM:
        sys.exit(0)
    else:
        sys.exit(1)


# Gracefully exit on the SIGTERM signal. This is usually sent by the parent process.
signal.signal(signal.SIGTERM, terminate_on_signal)

# Start the connection client.
client.start()
