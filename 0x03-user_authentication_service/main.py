#!/usr/bin/env python3
"""
Test module:
    register_user(email: str, password: str) -> None
    log_in_wrong_password(email: str, password: str) -> None
    log_in(email: str, password: str) -> str
    profile_unlogged() -> None
    profile_logged(session_id: str) -> None
    log_out(session_id: str) -> None
    reset_password_token(email: str) -> str
    update_password(email: str, reset_token: str, new_password: str) -> None
"""
import requests


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    """test the register user functionality"""
    url = "http://localhost:5000/users"
    with requests.post(url, {"email": email, "password": password}) as resp:
        assert resp.status_code == 200
        expected_response = {
            "email": email,
            "message": "user created"
        }
        assert resp.json() == expected_response


def log_in_wrong_password(email: str, password: str) -> None:
    """test login with a wrong password"""
    url = "http://localhost:5000/sessions"
    with requests.post(url, {'email': email, 'password': password}) as resp:
        assert resp.status_code == 401


def log_in(email: str, password: str) -> str:
    """test the """
    url = "http://localhost:5000/sessions"
    with requests.post(url, {'email': email, 'password': password}) as resp:
        assert resp.status_code == 200
        expected_response = {
            "email": email,
            "message": "logged in"
        }
        assert resp.json() == expected_response
        assert resp.cookies.get('session_id')

        return resp.cookies.get('session_id')


def profile_unlogged() -> None:
    """ test the profile"""
    url = "http://localhost:5000/profile"
    with requests.get(url) as resp:
        assert resp.status_code == 403


def profile_logged(session_id: str) -> None:
    """test logged profile"""
    cookies = {
        'session_id': session_id
    }
    url = "http://localhost:5000/profile"
    with requests.get(url, cookies=cookies) as resp:
        assert resp.status_code == 200
        expected_response = {
            "email": EMAIL
        }
        assert expected_response == resp.json()


def log_out(session_id: str) -> None:
    """test the logout functionality"""
    url = "http://localhost:5000/sessions"
    cookies = {
        'session_id': session_id
    }
    with requests.delete(url, cookies=cookies) as resp:
        assert resp.status_code == 200


def reset_password_token(email: str) -> str:
    """test the reset_password"""
    url = "http://localhost:5000/reset_password"
    with requests.post(url, {"email": email}) as resp:
        assert resp.status_code == 200
        assert resp.json().get('reset_token')

        return resp.json().get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """test the update password functionality"""
    url = "http://localhost:5000/reset_password"
    data = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
    }
    with requests.put(url, data=data) as resp:
        assert resp.status_code == 200
        expected_response = {
            "email": email,
            "message": "Password updated"
        }
        assert expected_response == resp.json()


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
