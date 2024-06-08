#!/usr/bin/env python3
"""Module to test new error handle"""
from flask import Blueprint, abort, jsonify


app_views = Blueprint("app_views", __name__)


@app_views.route("/api/v1/status", methods=['GET'], strict_slashes=False)
def status() -> str:
    """Function to get the status of the API"""
    return jsonify({"status": "OK"})


@app_views.route("/api/v1/unauthorized", methods=["Get"], strict_slashes=False)
def unauthorized() -> str:
    """Function to get the status code"""
    return abort(401)


@app_views.route("/api/v1/forbidden", methods=["GET"], strict_slashes=False)
def forbidden() -> str:
    """Function to abort with status 403"""
    return abort(403)


@app_views.route("/api/v1/stats/", methods=["GET"], strict_slashes=False)
def stats() -> str:
    """Function to get the number of each objects"""
    from models.user import User
    stats = {}
    stats['users'] = User.count()
    return jsonify(stats)
