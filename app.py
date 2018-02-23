from FlaskHelpers import FlaskHelpers
from flask import Flask

app = Flask(__name__)
flask_helpers = FlaskHelpers()


@app.route("/")
def index():
    return flask_helpers.message('woops... It seems that you got the wrong place', 404)


@app.route("/upload")
def upload():
    return flask_helpers.message('Not supported for now but will be :).')
