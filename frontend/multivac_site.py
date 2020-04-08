import logging

from flask import Flask, make_response, render_template, request

import frontend.frontend_constants as constants

from agents.agent_registry import AGENTS
from environment.environment_registry import ENVIRONMENTS
from session import static_configs
from session.session_starter import start_multivac_session
from session.session_status_enum import SessionStatusEnum


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

# Gather options for environment name
ENVIRONMENT_NAME_OPTIONS = sorted(ENVIRONMENTS.keys())

# Gather options for agent name
AGENT_NAME_OPTIONS = sorted(AGENTS.keys())


@app.route('/', methods=['GET', 'POST'])
def route_index_page():
    """
    This is the main routing function for the Multivac page.

    For a POST request, assume the launcher form has been submitted and render the session page.
    For a GET request or any other request, render the launcher form.
    """

    if request.method == 'POST':
        try:
            environment_name, agent_name, num_steps, observation_delta, video_fps = \
                validate_and_retrieve_multivac_params_from_request_form()
        except Exception as e:
            logger.error("Error processing user POST request to / endpoint: {}".format(e))
            return make_response(constants.INVALID_POST_PARAMETERS_DESIGNATION, 400)

        return render_session_page(environment_name, agent_name, num_steps, observation_delta, video_fps)
    else:
        return render_index_form_page()


@app.route('/session', methods=['POST'])
def route_session_page():
    """
    Launch the Multivac session with passed in parameters. Once completed, return a response indicating whether the
    session successfully completed.
    """

    try:
        environment_name, agent_name, num_steps, observation_delta, video_fps = \
            validate_and_retrieve_multivac_params_from_request_form()
    except Exception as e:
        logger.error("Error processing user POST request to /session endpoint: {}".format(e))
        return make_response(constants.INVALID_POST_PARAMETERS_DESIGNATION, 400)

    # Start session with passed in parameters
    logger.info(
        """
        Starting Multivac session with parameters:
          1. Environment name: {}
          2. Agent name: {}
          3. Num steps: {}
          4. Observation delta: {}
          5. Video FPS: {}
        """.format(environment_name, agent_name, num_steps, observation_delta, video_fps)
    )

    status = start_multivac_session(
        environment_name=environment_name,
        agent_name=agent_name,
        num_steps=num_steps,
        observation_delta=observation_delta,
        video_fps=video_fps
    )

    if status == SessionStatusEnum.SUCCESS:
        return make_response(constants.SUCCESS_DESIGNATION, 200)
    else:
        return make_response(constants.FAILED_DESIGNATION, 500)


def render_index_form_page():
    """
    Render the index.html template containing the launcher form.
    """

    return render_template(
        constants.INDEX_HTML,
        environment_name_options=ENVIRONMENT_NAME_OPTIONS,
        agent_name_options=AGENT_NAME_OPTIONS,
        max_num_steps=static_configs.MAX_NUM_STEPS,
        max_observation_delta=static_configs.MAX_OBSERVATION_DELTA,
        max_video_fps=static_configs.MAX_VIDEO_FPS
    )


def render_session_page(environment_name, agent_name, num_steps, observation_delta, video_fps):
    """
    Render the session.html page. This page will show placeholder HTML with an associated jquery script to send a
    request to the session endpoint.

    :param environment_name: Name of the environment for the session.
    :param agent_name: Name of the agent to use for the session.
    :param num_steps: Number of steps the agent should take during the session.
    :param observation_delta: Observation delta for the session.
    :param video_fps: Frames per second output video should be generated with.
    """

    # Session page currently displays simple text indicating session is running.
    return render_template(
        constants.SESSION_HTML,
        environment_name=environment_name,
        agent_name=agent_name,
        num_steps=num_steps,
        observation_delta=observation_delta,
        video_fps=video_fps
    )


def validate_and_retrieve_multivac_params_from_request_form():
    """
    Read in post parameters. If key is not located in the request or cannot be cast to the appropriate type,
    this will raise an exception.

    :return: multivac parameters: environment name, agent name, num steps, observation delta, video fps
    """

    environment_name = request.form[constants.ENVIRONMENT_NAME_KEY]
    agent_name = request.form[constants.AGENT_NAME_KEY]
    num_steps = int(request.form[constants.NUM_STEPS_KEY])
    observation_delta = int(request.form[constants.OBSERVATION_DELTA_KEY])
    video_fps = int(request.form[constants.VIDEO_FPS_KEY])

    return environment_name, agent_name, num_steps, observation_delta, video_fps


if __name__ == '__main__':
    app.run()
