#!/usr/bin/env python3
"""Module route of api unauthorized"""
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
from api.v1.views.index import app_views
import os
from os import getenv
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from typing import Literal, Optional


app = Flask(__name__)
CORS(app)
app.register_blueprint(app_views)
auth = None

if getenv("AUTH_TYPE") == "auth":
    from api.v1.auth.auth import Auth
    auth = Auth()

if getenv("AUTH_TYPE") == "basic_auth":
    from api.v1.auth.basic_auth import Auth
    auth = BasicAuth()


@app.before_request
def request_filter() -> None:
    """Function to check for requests authorization"""
    excluded_paths = [
        '/api/v1/status/',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden/'
        ]

    if auth:
        if auth.require_auth(request.path, excluded_paths):
            if auth.authorization_header(request) is None:
                abort(401)
            if auth.current_user(request) is None:
                abort(403)


@app.errorhandler(401)
def unauthorized(error) -> tuple[str, Literal[401]]:
    """Function to define and return error for unauthorized"""
    outcome = jsonify({"error": "Unauthorized"})
    outcome.status_code = 401
    return outcome


@app.errorhandler(403)
def forbidden(error) -> tuple[str, Literal[403]]:
    """FUnction to forbid authorization"""
    outcome = jsonify({"error": "Forbidden"})
    outcome.status_code = 403
    return outcome


@app.errorhandler(404)
def not_found(error) -> tuple[str, Literal[404]]:
    """Function to return a not found on request"""
    outcome = jsonify({"error": "Not found"})
    outcome.status_code = 404
    return outcome


@app.before_request
def before_request() -> Optional[str]:
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
