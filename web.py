import json
import os
import os.path
import tempfile
import requests

from flask import Flask, request, make_response, render_template, Response
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from flask_wtf.file import FileField, FileAllowed
from werkzeug import secure_filename
from wtforms import PasswordField, RadioField, TextField
from wtforms.validators import DataRequired

from tasks import process_user_csv, process_access_levels_csv
from access_levels import dump_access_levels_csv


app = Flask(__name__)

# TODO put them somewhere secure
app.config["UPLOAD_FOLDER"] = tempfile.gettempdir()
app.config["SECRET_KEY"] = os.environ.get('XIT_SECRET', 'secret-key')

bs = Bootstrap()
bs.init_app(app)


class CsvUploadForm(Form):
    xplan_url = TextField(
        'XPLAN URL',
        validators=[DataRequired()])
    xplan_username = TextField(
        'Username',
        validators=[DataRequired()])
    xplan_password = PasswordField(
        'Password',
        validators=[DataRequired()])
    csv_type = RadioField(
        'CSV Type',
        choices=(('users', 'Upload a CSV of new users'), ('access_levels', ' Upload a CSV of new and existing Access Levels')),
        default='users',
        validators=[DataRequired()])
    file = FileField('CSV File', validators=[
        DataRequired(),
        FileAllowed(
            ('csv',),
            ('Only CSV files can be uploaded for this field'))])


@app.route("/task/<task>")
def task(task):
    result = process_user_csv.AsyncResult(task)

    if result.ready():
        if isinstance(result.result, Exception):
            # TODO maybe only leak this in debug?
            return make_response(str(result.result), 500)

        return Response(response=json.dumps(result.result),
                status=200, mimetype="application/json")

    return Response(json.dumps({
        "state": result.state,
    }), status=102, mimetype="application/json")


@app.route("/upload_csv/<csv_type>", methods=["POST"])
def upload_csv(csv_type):
    arg_names = "xplan_url", "xplan_username", "xplan_password"
    try:
        args = [ request.form[arg_name] for arg_name in arg_names ]
    except KeyError as ex:
        return make_response("Missing param: %s" % ex, 400)

    try:
        file = request.files["file"]
    except KeyError as ex:
        return make_response("Missing file field", 400)

    if csv_type == "users":
        task = process_user_csv
    elif csv_type == "access_levels":
        task = process_access_levels_csv
    else:
        return make_response("Unknown CSV type", 404)

    filename = secure_filename(file.filename)
    path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(path)
    args.append(path)

    async_result = task.delay(*args)
    return make_response(str(async_result.id), 200)


@app.route("/access_levels.csv")
def dump_access_levels():
    arg_names = "xplan_url", "xplan_username", "xplan_password"
    try:
        args = [ request.args[arg_name] for arg_name in arg_names ]
    except KeyError as ex:
        return make_response("Missing param: %s" % ex[0], 400)

    try:
        return Response(response=dump_access_levels_csv(*args), status=200, mimetype="text/csv")
    except requests.HTTPError as ex:
        if ex.response.status_code == 401:
            return make_response("Invalid XPLAN username or password", 401)
        else:
            return make_response("Error talking to XPLAN", 500)


@app.route("/")
def home():
    form = CsvUploadForm()
    template_vars = dict(
        form=form)

    return render_template("home.html",
                           **template_vars)


if __name__ == "__main__":
    app.debug = 1
    app.run()
