import os
from werkzeug.utils import secure_filename
from FlaskHelpers import FlaskHelpers
from flask import Flask
from flask import request
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
flask_helpers = FlaskHelpers()


@app.route("/")
def index():
    return flask_helpers.message('woops... It seems that you got the wrong place', 404)


@app.route("/upload", methods=['POST'])
def upload():

    for file in dict(request.files):
        current_file = request.files[file]

        # Todo: handle when a file already exists.
        path = os.getcwd() + '/uploads/' + secure_filename(current_file.filename)
        current_file.save(path)
        return flask_helpers.response(response={'file': path})


@app.route("/process_file", methods=['POST'])
def process():
    return flask_helpers.message('Wait for it')
