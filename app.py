import os
from werkzeug.utils import secure_filename
from BismarkPusher import BismarkPusher
from FlaskHelpers import FlaskHelpers
from flask import Flask
from flask import request
from flask_cors import CORS
import pandas as pd
from bismarck_report import BismarckReport
from models.Results import Results

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


@app.route("/process_files", methods=['POST'])
def process():

    parsed_request = dict(request.form)

    if 'files' not in parsed_request.keys():
        return flask_helpers.error('The files property is empty.')

    if 'room' not in parsed_request.keys():
        return flask_helpers.error('You need to provide the pusher room.')

    if parsed_request['files'] is None:
        return flask_helpers.error('The files object is empty.')

    pusher = BismarkPusher(parsed_request['room'])

    reports = {}
    for file in parsed_request['files']:
        if file == '':
            continue

        file_split = file.split('/')
        file_name = file_split[-1]

        pusher.send_message(event='processing_file', message=file_name)

        pandas_excel = pd.ExcelFile(file)
        b_report = BismarckReport(pandas_excel)
        b_report.process_book()

        reports[file_name] = b_report.general_errors

    # Saving the results inside the DB.
    results = Results()
    document = results.insert({'results': reports})

    pusher.send_message(event='done', message=document)

    return flask_helpers.response(response={'data': document})
