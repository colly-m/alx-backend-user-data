#!/usr/bin/env python3
"""Module to test new error handle"""
from flask import Blueprint, abort


app_views = Blueprint("app_views", __name__)


@app_views.route("/api/v1/unauthorized", method=["Get"], strict_slashes=False)
def unauthorized() -> str:
    """Function to get the status code"""
    return abort(401)


@app_views.route("/api/v1/forbidden", method=["GET"], strict_slashes=False)
def forbidden() -> str:
    """Function to abort with status 403"""
    return abort(403)
