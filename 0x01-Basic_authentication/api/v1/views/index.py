#!/usr/bin/env python3
"""Module to test new error handle"""
from flask import Blueprint, abort


app_views = Blueprint("app_views", __name__)


@app_views.route("/api/v1/unauthorized", method=["Get"])
def unauthorized():
    """Function toget the status code"""
    abort(401)
