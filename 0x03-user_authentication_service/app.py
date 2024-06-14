#!/usr/bin/env python3
"""Module to setup a basic flask app"""
from flask import Flask, jsonify, request, abort
from auth import Auth


app = Flask(__name__)

AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def home() -> str:
    """Function to return a json message"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> str:
    """Function to the data form of users"""
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        return jsonify({"message": "email and password are required"}), 400

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """Function for login session"""
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        abort(401)

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)

    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)

    return response

@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """Function to a session logout"""
    session_id = request.cookies.get("session_id")

    if not session_id:
        abort(403)

    user = AUTH.get_user_by_session(session_id)

    if not user:
        abort(403)

    AUTH.destroy_session(session_id)

    return redirect("/")



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
