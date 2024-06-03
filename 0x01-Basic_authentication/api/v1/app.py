#!/usr/bin/env python3
"""Module route of api unauthorized"""
from flask import Flask, jsonify, abort
from api.v1.views.index import app_views


app = Flask(__name__)

app.register_blueprint(app_views)


@app.errorhandler(401)
def unauthorizedError(error) -> str:
    """Function to define and return error for unauthorized"""
    outcome = jsonify({"error": "Unauthorized"})
    outcome.status_code = 401
    return outcome


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
