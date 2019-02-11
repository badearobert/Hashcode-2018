#! usr/bin/python
import os
import uuid
from flask import Flask, render_template, redirect, url_for, send_from_directory, flash, jsonify, make_response, send_file
from flask_restful import Api, Resource, request
from pathlib import Path
from ProblemSolver import Solver
from Database import db, DatabaseHandler, SessionHandler
from JsonCreator import JsonCreator
from SessionStore import SessionStore

ALLOWED_EXTENSIONS = set(['out'])

# config settings
app = Flask(__name__)
app.config['IN_FOLDER'] = 'in'
app.config['OUT_FOLDER'] = 'out'
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB file max
app.secret_key = '43Gefa46g$256&92][;''42\p;'
app.config['UPLOAD_FOLDER'] = 'uploads'

# database settings
project_dir = os.path.dirname(os.path.abspath(__file__))
db_scores = "sqlite:///{}".format(os.path.join(project_dir, "scores.db"))
db_sessions = "sqlite:///{}".format(os.path.join(project_dir, "sessions.db"))
app.config["SQLALCHEMY_DATABASE_URI"] = db_scores

app.config["SQLALCHEMY_BINDS"] = {
    'sql_scores': db_scores,
    'sql_sessions': db_sessions
}

with app.app_context():
    db.init_app(app)
api = Api(app)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def fail(error):
    print("In fail!")
    alias = SessionHandler.get(request.remote_addr)
    global_results = DatabaseHandler.get_entries()
    return render_template('index.html', error=error, global_results=global_results, alias=alias)


def success(alias, index, global_results=None, local_results=None):
    return render_template('index.html', error=None, global_results=global_results, results=local_results, alias=alias, index=index), 200


def success_with_cookie(alias, pw):
    #resp = make_response(render_template('index.html', alias=alias))
    resp = make_response(redirect('/'))
    resp.set_cookie('password', pw)
    return resp


def get_input_path(filename):
    try:
        location = app.config['IN_FOLDER']
        filename = Path(filename).stem + ".in"
    except:
        print("Filename not found:" + filename)
        return ''
    return os.path.join(location, filename)


def upload_file(file, path):
    file.save(os.path.join(path, file.filename))


def create_upload_path(alias, upload_entry):
    path = os.path.join(app.config['UPLOAD_FOLDER'], str(alias), str(upload_entry))
    if not os.path.exists(path):
        os.makedirs(path)

    print("path is: {0}".format(path))
    return path


def read(full_path):
    try:
        print("attempting to read" + full_path)

        with open(full_path, 'r') as fp:
            data = fp.readlines()
            data = [x.strip() for x in data]
            # os.remove(full_path)
        return data
    except FileNotFoundError as e:
        print(str(e))
        raise e


@app.route("/register", methods=['GET', 'POST'])
def register():
    alias = ''

    cookie = request.cookies.get('password')
    if cookie is not None and cookie is not '' and cookie is not "":
        print("An attempt has been made to reach this page with a cookie set! Get out!")
        #return redirect(url_for('render'))

    if request.method == 'POST':
        if 'alias' in request.form:
            form_alias = request.form['alias']
            if form_alias == '':
                return render_template('register.html'), 200
            else:
                alias = form_alias
                print("alias is now {0}".format(alias))
        else:
            print("Alias not found in the request form!!!!")
            return render_template('register.html'), 200

        cookie = str(uuid.uuid4())
        print("Cookie for alias {0} set to {1}".format(alias, cookie))
        SessionHandler.add(alias, cookie)
        return success_with_cookie(alias, cookie)

    return render_template('register.html', alias=alias), 200


@app.route("/<alias>/<upload_entry>/<file_name>", methods=['GET', 'POST'])
def download_json_out(alias, upload_entry, file_name):
    path = create_upload_path(alias, upload_entry)
    return send_file(os.path.join(path, file_name + ".json"), as_attachment=True)
    # return render_template('visualization.html', formdata=path), 200


@app.route("/visualization", methods=['GET', 'POST'])
def redirect_visualization():
    return render_template('visualization.html'), 200


@app.route("/sessionz", methods=['GET'])
def get_sessions():
    sessions = SessionHandler.get_entries()
    return render_template('sessions.html', sessions=sessions), 200


@app.route('/', methods=['GET', 'POST'])
def render():
    local_results = []
    atomic_index = 1  # set this for having it in GET requests

    # check session or redirect to register
    SessionHandler.print()
    alias = ""
    cookie = request.cookies.get('password')
    if cookie is None:
        print("No cookie!")
    else:
        alias = SessionHandler.get(cookie)

    print("alias is {0}".format(alias))
    if alias is None or alias is "":
        #return fail('Please set an alias')
        return redirect(url_for('register'))

    if request.method == 'POST':
        # check uploaded files
        if len(request.files) == 0:
            return fail('No files were uploaded')

        # creating a new, atomic value for this upload
        atomic_index = SessionStore.fetch_add()
        for file in request.files.getlist("file[]"):
            if not allowed_file(file.filename):
                return fail('That file type is not supported')

            path = create_upload_path(alias, atomic_index)
            upload_file(file, path)
            try:
                # getting results from file
                data_input = read(get_input_path(file.filename))
                data_output = read(os.path.join(path, file.filename))  #read(get_file_path(file.filename, False))

                # creating the solver and fetching results
                solver = Solver(data_input, data_output)
                results = solver.get_points()

                # set results in local and global db
                local_results.append([file.filename, results])
                DatabaseHandler.set(alias, file.filename, results)

                #  storing json and uploading as well
                jc = JsonCreator(file.filename, solver.obj_in)
                jc.create_json(path)

            except Exception as e:
                return fail(str(e))

    return success(alias, atomic_index, DatabaseHandler.get_entries(), local_results)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
    #app.run(host='0.0.0.0', port=8080, debug=True)
    #app.run(host='0.0.0.0', debug=True, threaded=True)