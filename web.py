from flask import Flask, request, make_response, Response
import json
import flask
from tasks import process_user_csv, process_access_levels_csv
from access_levels import dump_access_levels_csv
from werkzeug import secure_filename
import os.path
import tempfile

app = Flask(__name__)

# TODO put them somewhere secure
app.config["UPLOAD_FOLDER"] = tempfile.gettempdir()

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
def upload_user_csv(csv_type):
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


@app.route("/access_levels")
def dump_access_levels():
    arg_names = "xplan_url", "xplan_username", "xplan_password"
    try:
        args = [ request.args[arg_name] for arg_name in arg_names ]
    except KeyError as ex:
        return make_response("Missing param: %s" % ex[0], 400)

    return Response(response=dump_access_levels_csv(*args), status=200, mimetype="text/csv")


if __name__ == "__main__":
    app.debug = 1
    app.run()
