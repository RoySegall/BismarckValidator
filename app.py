import os
from werkzeug.utils import secure_filename
from BismarkPusher import BismarkPusher
from FlaskHelpers import FlaskHelpers
from flask import Flask, url_for, render_template
from flask import request
from flask_cors import CORS
from report_processor.bismarck_report import BismarckReport
from models.Results import Results
from rosetta.rosetta_config import RosettaConfig
import rollbar
import rollbar.contrib.flask
from flask import got_request_exception
import yaml

app = Flask(__name__, static_url_path='/dist')
cors = CORS(app, resources={r"/*": {"origins": "*"}})
flask_helpers = FlaskHelpers()

@app.before_first_request
def init_rollbar():
    print('a')

    stream = open(os.getcwd() + "/rollbar.yml")
    rollbar_settings = yaml.load(stream)

    print(rollbar_settings)
    """init rollbar module"""
    rollbar.init(
        # access token for the demo app: https://rollbar.com/demo
        rollbar_settings['key'],
        # environment name
        rollbar_settings['env'],
        # server root directory, makes tracebacks prettier
        root=os.path.dirname(os.path.realpath(__file__)),
        # flask already sets up logging
        allow_logging_basic_config=False)

    # send exceptions from `app` to rollbar, using flask's signal system.
    got_request_exception.connect(rollbar.contrib.flask.report_exception, app)


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


@app.route("/process_files", methods=['POST'])
def process():
    parsed_request = dict(request.form)

    # A couple of validations.
    if 'files' not in parsed_request.keys():
        return flask_helpers.error('The files property is empty.')

    if 'room' not in parsed_request.keys():
        return flask_helpers.error('You need to provide the pusher room.')

    if parsed_request['files'] is None:
        return flask_helpers.error('The files object is empty.')

    # Init variables.
    pusher = BismarkPusher(parsed_request['room'])
    reports = {}

    for file in parsed_request['files'][0].split(","):
        if file == '':
            continue

        # Get the file name.
        file_split = file.split('/')
        file_name = file_split[-1]

        # Notify the user we started to process.
        pusher.send_message(event='processing_file', message=file_name)

        # Check out the new api to bismark report
        b_report = BismarckReport(report_file_name=file)
        b_report.process_book()
        reports[file_name] = b_report.get_compact()

    # Saving the results inside the DB.
    results = Results()
    document = results.insert({'results': reports})

    # Done!
    # pusher.send_message(event='done', message=document)
    return flask_helpers.response(response={'data': document})


@app.route("/process_files/<id>", methods=['GET'])
def process_files_results(id):
    """
    Return the results for process files.

    :param id:
        The ID of the process.

    :return:
        The object in the DB.
    """
    results = Results()
    return flask_helpers.response(results.load(id))


@app.route("/metadata", methods=['GET'])
def metadata():
    rosetta = RosettaConfig()
    return flask_helpers.response({
        'fields': flask_helpers.flip_dict(rosetta.FIELDS_LIST),
        'instruments': flask_helpers.flip_dict(rosetta.INSTRUMENT_DICT)
    })
