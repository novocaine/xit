"""
REST API handlers intended for AJAX use
"""

import json
import os.path

import requests
from flask import make_response, Response, request, current_app
from werkzeug.utils import secure_filename

from xit.access_levels import dump_access_levels_csv
from xit.tasks import process_user_csv, process_access_levels_csv

from flask import Blueprint

blueprint = Blueprint('api', __name__, static_folder="../static")


@blueprint.route("/task/<task>")
def task(task):
    result = process_user_csv.AsyncResult(task)

    if result.ready():
        if isinstance(result.result, Exception):
            # TODO maybe only leak this in debug?
            return make_response(str(result.result), 500)

        return Response(response=json.dumps(result.result),
                status=200, mimetype="application/json")

    return Response(response=json.dumps({
        "state": result.state,
    }), status=202, mimetype="application/json")


@blueprint.route("/upload_csv/<csv_type>", methods=["POST"])
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
    path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    file.save(path)
    args.append(path)

    async_result = task.delay(*args)
    return make_response(str(async_result.id), 200)


@blueprint.route("/access_levels.csv")
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