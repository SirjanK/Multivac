import sys
import os

# Hacky workaround for now. TODO: Fix
sys.path.append("/home/sirjan/Projects/SymphonicaUltima")

# Another hacky workaround.
sys.path.append("/home/sirjan/Applications/redis-py-2.10.6")

from device.connection_client import ConnectionClient


if __name__ == '__main__':
    # Blow away the out directory.
    out_path = "./out"
    if os.path.exists(out_path):
        for file in os.listdir(out_path):
            os.remove(out_path + "/" + file)

    # Initialize the connection client.
    client = ConnectionClient(2000, 2)

    client.start_action_input()
    client.stream_observations()
    client.wait(10)
