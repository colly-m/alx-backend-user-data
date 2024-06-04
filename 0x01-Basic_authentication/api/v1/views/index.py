#!/usr/bin/env python3
"""Module to test new error handle"""
from flask import Blueprint, abort


app_views = Blueprint("app_views", __name__)


@app_views.route("/api/v1/unauthorized", method=["Get"])
def unauthorized():
    """Function to get the status code"""
    abort(401)



@app_views.route("/api/v1/forbidden", method=["GET"])
def forbidden():
    """Function to abort with status 403"""
    abort(403)
