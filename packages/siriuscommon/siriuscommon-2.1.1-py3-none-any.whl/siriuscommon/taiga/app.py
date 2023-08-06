#!/usr/bin/env python

import csv
import io
import json

import requests

from flask import Flask, Response, request

BASE_API_URL = "https://10.0.38.59:9011/api/v1"
BASE_TASKS = f"{BASE_API_URL}/tasks/csv"
BASE_USER_STORY = f"{BASE_API_URL}/userstories/csv"

app = Flask(__name__)


def load_data(url, params):
    return io.StringIO(
        requests.get(url, params=params, verify=False).content.decode("utf8")
    )


@app.route("/taiga/tasks", methods=["GET"])
def tasks():
    uuid = request.args.get("uuid")
    if not uuid:
        return "Missing param uuid", 400

    csv_f = load_data(BASE_TASKS, params={"uuid": uuid})
    return Response(
        json.dumps(list(csv.DictReader(csv_f))), mimetype="application/json"
    )


@app.route("/taiga/stories", methods=["GET"])
def stories():
    uuid = request.args.get("uuid")
    if not uuid:
        return "Missing param uuid", 400

    csv_f = load_data(BASE_USER_STORY, params={"uuid": uuid})
    return Response(
        json.dumps(list(csv.DictReader(csv_f))), mimetype="application/json"
    )


if __name__ == "__main__":
    app.run(debug=True)
