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

@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile():
    """Function to get session ID from cookies"""
    session_id = request.cookies.get("session_id")

    if not session_id:
        abort(403)

    user = AUTH.get_user_by_session(session_id)

    if not user:
        abort(403)

    return jsonify({
        "email": user.email,
        "name": user.name,
        "birthdate": user.birthdate,
        "address": user.address
    })


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token():
    """Function to get form data to reset password"""
    email = request.form.get("email")

    if not email:
        abort(403)

    if not AUTH.email_registered(email):
        abort(403)

    reset_token = AUTH.generate_reset_token(email)

    return jsonify({
        "email": email,
        "reset_token": reset_token
    }), 200


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password():
    """Function to get form data to update a new password session"""
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    if not email or not reset_token or not new_password:
        abort(403)

    try:
        AUTH.verify_reset_token(email, reset_token)

        AUTH.update_password(email, new_password)

        return jsonify({
            "email": email,
            "message": "Password updated"
        }), 200
    except ValueError:
        abort(403)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
