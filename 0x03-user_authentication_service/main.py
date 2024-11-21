#!/usr/bin/env python3
"""
    Testing:->
        register_user(email: str, password: str) -> None
        log_in_wrong_password(email: str, password: str) -> None
        log_in(email: str, password: str) -> str
        profile_unlogged() -> None
        profile_logged(session_id: str) -> None
        log_out(session_id: str) -> None
        reset_password_token(email: str) -> str
        update_password(email: str, reset_token: str,
        new_password: str) -> None
"""

import requests


def register_user(email: str, password: str) -> None:
    """
        Test case: Auth.register_user
        assert: re
    """
    payload = {
        'email': email,
        'password': password
    }
    response = requests.post('http://127.0.0.1:5000/users', data=payload)
    assert response.json() == {"email": email, "message": "user created"}
    assert response.status_code == 200


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Test case: Auth.valid_login,
    Route: /sessions, login_logout(function)
    """
    payload = {
        'email': email,
        'password': password
    }
    response = requests.post('http://127.0.0.1:5000/sessions', data=payload)
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """
       Test case: Auth.valid_login,
                Route: /sessions, login_logout(function)
    """
    payload = {
        'email': email,
        'password': password
    }

    response = requests.post('http://127.0.0.1:5000/sessions', data=payload)
    assert response.json() == {"email": email, "message": "logged in"}
    assert response.status_code == 200
    return response.cookies.get('session_id')


def profile_unlogged() -> None:
    """
     Profile -> logged_out
    """

    response = requests.delete('http://127.0.0.1:5000/sessions')
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """
        Profile logged
    """
    cookies = {
        'session_id': session_id
    }

    response = requests.get('http://127.0.0.1:5000/profile', cookies=cookies)
    assert response.status_code == 200


def log_out(session_id: str) -> str:
    """ Logout test
    """
    cookies = {
        'session_id': session_id
    }

    response = requests.delete('http://127.0.0.1:5000/sessions',
                               cookies=cookies)
    assert response.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """Reset password
    """
    payload = {
        'email': email
    }
    response = requests.post('http://127.0.0.1:5000/reset_password',
                             data=payload)
    print()
    assert response.json().get('email') == email
    return response.json().get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Update
        test
    """
    payload = {
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password
    }

    response = requests.put('http://127.0.0.1:5000/reset_password',
                            data=payload)
    assert response.json() == {"email": email,
                               "message": "Password updated"}
    assert response.status_code == 200


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
