import os
from device.time_manager import TimeManager


def parse_args(args):
    pass


def init_redis():
    pass


def start_connection_client():
    pass


def start_ultima():
    pass


if __name__ == '__main__':
    print("Starting session.")

    TimeManager.get_default_instance().start()

    # Run the connection_client.
    # TODO: Parameter parsing to get monkerunner path
    monkeyrunner_cmd = "~/Android/Sdk/tools/bin/monkeyrunner"
    os.system(monkeyrunner_cmd + " " + "device/connection_client_starter.py")
