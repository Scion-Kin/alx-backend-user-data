#!/usr/bin/env python3
"""
Main file
"""

import requests


url = 'http://0.0.0.0:5000/'


def register_user(email: str, password: str) -> None:
    ''' Tests the /users endpoint '''

    res = requests.post(url + 'users', data={"email": email,
                                             "password": password})
    assert res.status_code == 200


def log_in_wrong_password(email: str, password: str) -> None:
    ''' Tests a wrong login '''

    res = requests.post(url + 'sessions', data={"email": email,
                                                "password": password})
    assert res.status_code != 200


def log_in(email: str, password: str) -> str:
    ''' Tests correct login '''

    res = requests.post(url + 'sessions', data={"email": email,
                                                "password": password})
    assert res.status_code == 200

    return res.cookies.get('session_id')


def profile_unlogged() -> None:
    ''' Tests the /profile endpoint when not logged in '''

    res = requests.get(url + 'profile')
    assert res.status_code != 200


def profile_logged(session_id: str) -> None:
    ''' Tests the /profile endpoint when logged in '''

    res = requests.post(url + 'users', cookies={"session_id": session_id})
    assert res.status_code == 200


def log_out(session_id: str) -> None:
    ''' Tests the logout function '''

    res = requests.delete(url + 'sessions', cookies={"session_id": session_id})
    assert res.status_code == 200


def reset_password_token(email: str) -> str:
    ''' Tests the reset password function '''

    res = requests.post(url + 'reset_password', data={"email": email})
    assert res.status_code == 200

    return res.json()["reset_token"]


def update_password(email: str, reset_token: str, new_password: str) -> None:
    ''' Tests the update password function '''

    res = requests.put(url + 'reset_password',
                       data={"email": email,
                             "reset_token": reset_token,
                             "new_password": new_password})
    assert res.status_code == 200


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
