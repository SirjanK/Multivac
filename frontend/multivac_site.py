from flask import Flask, render_template

import frontend.frontend_constants as constants


app = Flask(__name__)


@app.route('/')
def render_index_page():
    return render_template(constants.INDEX_HTML)


if __name__ == '__main__':
    app.run()
