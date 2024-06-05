#!/usr/bin/env python3
"""Module route of api unauthorized"""
from flask import Flask, jsonify, abort, request
from flask_cors import CORS
from api.v1.views.index import app_views
import os
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth


app = Flask(__name__)
CORS(app)
app.register_blueprint(app_views)
auth = None

if getenv("AUTH_TYPE") == "auth":
    auth = Auth()
elif getenv("AUTH_TYPE") == "basic_auth":
    auth = BasicAuth()


@app.errorhandler(401)
def unauthorizedError(error) -> str:
    """Function to define and return error for unauthorized"""
    outcome = jsonify({"error": "Unauthorized"})
    outcome.status_code = 401
    return outcome


@app.errorhandler(403)
def forbid_error(error):
    outcome = jsonify({"error": "Forbidden"})
    outcome.status_code = 403
    return outcome


@app.before_request
def before_request(i):
    """Function to filter each request"""
    if auth is None:
        return

    excluded_paths = ['/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/']
    if not auth.require_auth(request.path, excluded_paths):
        return

    if auth.authorization_header(request) is None:
        abort(401)

    if auth.current_user(request) is None:
        abort(403)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
