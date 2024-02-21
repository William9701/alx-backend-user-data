#!/usr/bin/env python3
""" Main module
"""

import requests

BASE_URL = "http://127.0.0.1:5000"


def register_user(email: str, password: str) -> None:
    response = requests.post(f"{BASE_URL}/users",
                             data={"email": email, "password": password})
    assert response.status_code == 200, \
        f"Failed to register user: {response.text}"


def log_in_wrong_password(email: str, password: str) -> None:
    response = requests.post(f"{BASE_URL}/sessions",
                             data={"email": email, "password": password})
    assert response.status_code == 401,\
        f"Login with wrong password did not return 401: {response.text}"


def profile_unlogged() -> None:
    response = requests.get(f"{BASE_URL}/profile")
    assert response.status_code == 403,\
        f"Profile unlogged did not return 403: {response.text}"


def log_in(email: str, password: str) -> str:
    response = requests.post(f"{BASE_URL}/sessions",
                             data={"email": email, "password": password})
    assert response.status_code == 200,\
        f"Failed to log in: {response.text}"
    return response.cookies.get('session_id')


def profile_logged(session_id: str) -> None:
    headers = {"Cookie": f"session_id={session_id}"}
    response = requests.get(f"{BASE_URL}/profile", headers=headers)
    assert response.status_code == 200,\
        f"Profile logged did not return 200: {response.text}"


def log_out(session_id: str) -> None:
    headers = {"Cookie": f"session_id={session_id}"}
    response = requests.delete(f"{BASE_URL}/sessions", headers=headers)
    assert response.status_code == 302,\
        f"Logout did not return 302: {response.text}"


def reset_password_token(email: str) -> str:
    response = requests.post(f"{BASE_URL}/reset_password",
                             data={"email": email})
    assert response.status_code == 200,\
        f"Failed to get reset token: {response.text}"
    return response.json().get("reset_token")


def update_password(email: str, reset_token: str,
                    new_password: str) -> None:
    response = requests.put(f"{BASE_URL}/reset_password",
                            data={"email": email,
                                  "reset_token": reset_token,
                                  "new_password": new_password})
    assert response.status_code == 200,\
        f"Failed to update password: {response.text}"


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
