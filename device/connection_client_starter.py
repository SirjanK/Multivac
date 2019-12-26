"""
This is a starter script for the connection_client. It requires the following cmd line arguments in order:
  i) redispy path: local path to redispy library
  ii) port that redis server is running
  iii) observation delta: time in milliseconds after an action is taken to take a screenshot of the device.
It is best to call this using `session_starter.py`.
"""

import atexit
import os
import sys

redispy_path, redis_port, observation_delta = sys.argv[1:]

# Add the redispy (python 2.6 version) library.
sys.path.append(redispy_path)

# This is to ensure jython will have the current project in its path.
sys.path.append(os.getcwd())

from device.connection_client import ConnectionClient

assert(len(sys.argv) == 4, 'Three arguments required.')

# Initialize the connection client.
client = ConnectionClient(int(redis_port), int(observation_delta))

atexit.register(lambda: client.shutdown())

client.start()
