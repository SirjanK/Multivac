"""
The session_starter script can be run via command line by supplying relevant parameters. It also provides the
`start_multivac_session()` function to start the session from UI.

For list of parameters required when run from the command line, run `python session/session_starter.py -h`.
Run this script from the Multivac project directory.
"""


import argparse
import atexit
import json
import os
import subprocess

from agents.agent_registry import AGENTS
from environment.environment_registry import ENVIRONMENTS
from session.multivac import Multivac

# Input parameter keys.
# From config file
MONKEYRUNNER_PATH = "monkeyrunner_path"
REDISPY_PATH = "redispy_path"

# From command line
NUM_STEPS = "num-steps"
OBSERVATION_DELTA = "observation-delta"
ENVIRONMENT_NAME = "environment-name"
AGENT_NAME = "agent-name"
VIDEO_FPS = "video-fps"
DISPLAY_VIDEO = "display-video"

# Fixed paths
CFG_FILE_PATH = "run_config.json"
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
    :param monkeyrunner_path: Local path to the monkeyrunner bin.
    :param redispy_path: Local path to modified redis py library that is compatible with jython 2.5.
    :param redis_port: Port that the redis server is running in.
    :param observation_delta: Time interval between observations.
    :return Popen object corresponding to the process running the connection client.
    """
    connection_client_process = subprocess.Popen(
        [monkeyrunner_path, CONNECTION_CLIENT_STARTER_SCRIPT_PATH, redispy_path, str(redis_port),
         str(observation_delta)]
    )

    return connection_client_process


def parse_config_file():
    """
    Parse the config file located at CFG_FILE_PATH; raise exception if the file does not exist.
    :return: Path to monkeyrunner executable and path to redispy library.
    """
    assert os.path.exists(CFG_FILE_PATH), \
        "{} cannot be found. Make sure to specify config file".format(CFG_FILE_PATH)

    with open(CFG_FILE_PATH, 'r') as fp:
        cfg_contents = json.load(fp)

    monkeyrunner_path = cfg_contents[MONKEYRUNNER_PATH]
    redispy_path = cfg_contents[REDISPY_PATH]

    return monkeyrunner_path, redispy_path


def parse_args():
    """
    Parse cmd line arguments.
    :return: arguments that are accessible as args.PARAM_NAME
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('--' + ENVIRONMENT_NAME, type=str, required=True, choices=ENVIRONMENTS.keys(),
                        help="Name of the environment to start")
    parser.add_argument('--' + AGENT_NAME, type=str, required=True, choices=AGENTS.keys(),
                        help="Name of the agent to use")
    parser.add_argument('--' + NUM_STEPS, type=int, required=True,
                        help="Number of steps to take on the environment before terminating.")
    parser.add_argument('--' + OBSERVATION_DELTA, type=int, required=False, default=250,
                        help="Frame per second of the output recording of the gym environment. " +
                             "Each frame will be one observation image.")
    parser.add_argument('--' + VIDEO_FPS, type=int, required=False, default=1,
                        help="Frame per second of the output recording of the gym environment. " +
                             "Each frame will be one observation image.")
    parser.add_argument('--' + DISPLAY_VIDEO, default=False, action='store_true',
                        help="Flag to determine whether or not to manually display session in a window separate from "
                             "the device/emulator or UI.")

    return parser.parse_args()


def start_multivac_session(environment_name, agent_name, num_steps, observation_delta=250, video_fps=1,
                           display_video=False):
    """
    Start the Multivac session which includes:
      1. Starting a connection client with an Android device
      2. Starting a Multivac environment and agent to interface with the device

    :param environment_name: Name of the environment to use.
    :param agent_name: Name of the agent to use.
    :param num_steps: Number of steps to take on the environment.
    :param observation_delta: Time interval between observations.
    :param video_fps: Frame per second of the output recording of the gym environment.
    :param display_video: Flag to determine whether or not to manually display session in a window separate from the
                          device/emulator or UI.
    """
    # Gather information from config file
    monkeyrunner_path, redispy_path = parse_config_file()

    # Flush DB
    flush_redis_db()

    # Start Redis DB
    redis_process = start_redis_db()

    # Start connection client
    device_process = start_connection_client(
        monkeyrunner_path=monkeyrunner_path,
        redispy_path=redispy_path,
        redis_port=DEFAULT_REDIS_PORT,
        observation_delta=observation_delta
    )

    # Set up the Multivac
    multivac = Multivac(
        environment_name,
        agent_name,
        num_steps,
        redis_port=DEFAULT_REDIS_PORT,
        video_fps=video_fps,
        display_video=display_video
    )

    # Once this script terminates in any way, redis_process and device_process should terminate as well.
    def on_terminate():
        device_process.terminate()
        redis_process.terminate()
        flush_redis_db()

    atexit.register(on_terminate)

    # Launch the Multivac.
    multivac.launch()


if __name__ == '__main__':
    params = parse_args()

    start_multivac_session(
        environment_name=params.environment_name,
        agent_name=params.agent_name,
        num_steps=params.num_steps,
        observation_delta=params.observation_delta,
        video_fps=params.video_fps,
        display_video=params.display_video
    )
