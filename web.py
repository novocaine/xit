from flask import Flask
import flask
from tasks import add

app = Flask(__name__)

@app.route("/")
def hello():
    return add.delay(4, 4).id

@app.route("/task/<task>")
def task(task):
    result = add.AsyncResult(task)
    return flask.jsonify(**{
        "state": result.state,
        "info": result.info,
        "result": result.result if result.ready() else None
    })

if __name__ == "__main__":
    app.debug = 1
    app.run()
