#!/usr/bin/env python3
"""Module to test end-to-end intergration"""
import requests


def register_user(email: str, password: str) -> None:
    response = requests.post(f"/users", data={"email":
                             email, "password": password})
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    response = requests.post(f"/sessions", data={"email": email,
                             "password": password})
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    response = requests.post(f"/sessions", data={"email": email,
                             "password": password})
    assert response.status_code == 200
    session_id = response.cookies.get("session_id")
    assert session_id is not None
    return session_id


def profile_unlogged() -> None:
    response = requests.get(f"/profile")
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    cookies = {"session_id": session_id}
    response = requests.get(f"/profile", cookies=cookies)
    assert response.status_code == 200
    assert "email" in response.json()


def log_out(session_id: str) -> None:
    cookies = {"session_id": session_id}
    response = requests.delete(f"/sessions", cookies=cookies)
    assert response.status_code == 200


def reset_password_token(email: str) -> str:
    response = requests.post(f"/reset_password", data={"email": email})
    assert response.status_code == 200
    reset_token = response.json().get("reset_token")
    assert reset_token is not None
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    response = requests.put(f"/reset_password", data={"email": email,
                            "reset_token": reset_token,
                                                  "new_password": new_password})
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
