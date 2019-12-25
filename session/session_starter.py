"""
This is the starter script to launch a Multivac session. This entails two things:
  1. Starting a connection client with an Android device
  2. Starting a Multivac environment and agent to interface with the device
For list of parameters required, run `python -h session_starter.py`.
"""


import argparse
import subprocess

# Input parameter keys.
MONKEYRUNNER_PATH = "monkeyrunner-path"
REDISPY_PATH = "redispy-path"
MULTIVAC_VERSION = "multivac-version"
NUM_STEPS = "num-steps"
OBSERVATION_DELTA = "observation-delta"
ENVIRONMENT_NAME = "environment-name"
AGENT_NAME = "agent-name"

# Fixed paths
CONNECTION_CLIENT_STARTER_SCRIPT_PATH = "device/connection_client_starter.py"

DEFAULT_REDIS_PORT = 6379


def flush_redis_db():
    """
    Flush all existing data from redis to remove any pending actions and observations.
    """
    subprocess.run(["redis-cli", "flushall"])


def start_redis_db():
    """
    Starts the redis DB at the default port.
    :return Popen object corresponding to the child process running the redis server.
    """
    redis_server_process = subprocess.Popen(["redis-server"])
    return redis_server_process


def start_connection_client(monkeyrunner_path, redispy_path, redis_port, observation_delta):
    """
    Starts the connection client by invoking the starter script with appropriate parameters.
    :param monkeyrunner_path: Path to the monkeyrunner script.
    :param redispy_path: Path to modified redis py library that is compatible with jython 2.5.
    :param redis_port: Port that the redis server is running in.
    :param observation_delta: Time interval between observations.
    :return Popen object corresponding to the process running the connection client.
    """
    connection_client_process = subprocess.Popen(
        [monkeyrunner_path, CONNECTION_CLIENT_STARTER_SCRIPT_PATH, redispy_path, redis_port, observation_delta]
    )

    return connection_client_process


def run_multivac(version, session_time):
    """
    Starts the Multivac with specific version which determines the algorithm used.
    :param version: Integer >= 0 representing the Multivac version.
    :param session_time: Time to run the session.
    """
    # TODO implement
    pass


def parse_args():
    """
    Parse cmd line arguments.
    :return: arguments that are accessible as args[PARAM_NAME]
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('--' + MONKEYRUNNER_PATH, type=str, required=True,
                        help="Local filepath to installed monkeyrunner cmd")
    parser.add_argument('--' + REDISPY_PATH, type=str, required=True, help="Local filepath to installed redispy source")
    parser.add_argument('--' + ENVIRONMENT_NAME, type=str, required=True, choices=['a'],
                        help="Name of the environment to start")
    parser.add_argument('--' + AGENT_NAME, type=str, required=True, choices=['b'], help="Name of the agent to use")
    parser.add_argument('--' + NUM_STEPS, type=int, required=True,
                        help="Number of steps to take on the environment before terminating.")
    parser.add_argument('--' + OBSERVATION_DELTA, type=int, required=False, default=1000,
                        help="Time to wait in milliseconds after taking an action in order to take a screenshot")

    return parser.parse_args()


if __name__ == '__main__':
    params = parse_args()

    # Flush DB
    flush_redis_db()

    # Start Redis DB
    redis_process = start_redis_db()

    # Start connection client
    device_process = start_connection_client(
        monkeyrunner_path=params[MONKEYRUNNER_PATH],
        redispy_path=[REDISPY_PATH],
        redis_port=DEFAULT_REDIS_PORT,
        observation_delta=params[OBSERVATION_DELTA]
    )

    # Run the Multivac
    # run_multivac(params[MULTIVAC_VERSION], params[SESSION_TIME])

    # Terminate connection client once finished.
    device_process.terminate()

    # Flush DB once finished
    redis_process.terminate()
    flush_redis_db()
