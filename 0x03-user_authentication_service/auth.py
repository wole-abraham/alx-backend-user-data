#!/usr/bin/env python3
""" hashed passwords using bcrypt"""
import bcrypt
from db import DB
from sqlalchemy.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """
    password_string -> hashed_password
    bcrypt.hashpw
    """
    salt = bcrypt.gensalt()
    password = password.encode('utf-8')
    hash = bcrypt.hashpw(password, salt)
    return hash


class Auth:
    """Auth class to interact wiht the authentication database
    """

    def __init__(self):
        """__db = DB()

        """
        self._db = DB()

    def register_user(self, email, password):
        """ register user -> User <- email, password
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            hashed = _hash_password(password)
            user = self._db.add_user(email, hashed)
            return user
        else:
            raise ValueError(f"User <{email}> already exists")
