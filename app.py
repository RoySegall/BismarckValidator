import os
from werkzeug.utils import secure_filename
from FlaskHelpers import FlaskHelpers
from flask import Flask
from flask import request
from flask_cors import CORS
import pandas as pd
from bismarck_report import BismarckReport
import rethinkdb as r
from rethinkdb.errors import RqlRuntimeError

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
flask_helpers = FlaskHelpers()
g = None


@app.before_request
def before_request():
    try:
        g.rdb_conn = r.connect()
    except RqlRuntimeError:
        print("Database connection could be established.")


# close the connection after each request
@app.teardown_request
def teardown_request(exception):
    try:
        g.rdb_conn.close()
    except AttributeError:
        pass


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

    print(parsed_request)

    if 'files' not in parsed_request.keys():
        return flask_helpers.error('The files property is empty.')

    if parsed_request['files'] is None:
        return flask_helpers.error('The files object is empty.')

    reports = {}
    for file in parsed_request['files']:
        if file == '':
            continue

        pandas_excel = pd.ExcelFile(file)
        b_report = BismarckReport(pandas_excel)
        b_report.process_book()
        file_split = file.split('/')
        reports[file_split[-1]] = b_report.general_errors

    return flask_helpers.response(response={'results': reports})
