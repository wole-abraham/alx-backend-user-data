#!/usr/bin/env python3
""" hashed passwords using bcrypt"""
import bcrypt
from db import DB
from typing import Union
from user import User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """
    Hashes a plain-text password using bcrypt.
    Args:
        password (str): The plain-text password.
    Returns:
        bytes: The hashed password.
    """

    salt = bcrypt.gensalt()
    password = password.encode('utf-8')
    hash = bcrypt.hashpw(password, salt)
    return hash


class Auth:
    """Auth class to interact wiht the authentication database
    """

    def __init__(self):
        """
        Initializes the Auth instance with a database instance.
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> Union[None, User]:
        """
        Registers a user if the email does not already exist.
        Args:
            email (str): The user's email.
            password (str): The user's plain-text password.
        Returns:
            User: The created User object.
        Raises:
            ValueError: If the email is already registered.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            return self._db.add_user(email, hashed_password)

    def valid_login(self, email: str, password: str) -> bool:
        """
            Validate user and hashed password
        """
        try:
            user = self._db.find_user_by(email=email)
            password = password.encode('utf-8')
            return bcrypt.checkpw(password, user.hashed_password)
        except NoResultFound:
            return False
