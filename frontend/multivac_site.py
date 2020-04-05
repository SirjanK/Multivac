from flask import Flask, render_template

import frontend.frontend_constants as constants

from agents.agent_registry import AGENTS
from environment.environment_registry import ENVIRONMENTS


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route('/')
def render_index_page():
    # Gather options for environment name
    environment_name_options = sorted(ENVIRONMENTS.keys())

    # Gather options for agent name
    agent_name_options = sorted(AGENTS.keys())

    return render_template(
        constants.INDEX_HTML,
        environment_name_options=environment_name_options,
        agent_name_options=agent_name_options
    )


if __name__ == '__main__':
    app.run()
