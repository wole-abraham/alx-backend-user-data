#!/usr/bin/env python3
""" hashed passwords using bcrypt"""
import bcrypt
from db import DB
from typing import Union
from user import User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


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


def _generate_uuid() -> str:
    """_summary_

    Raises:
        ValueError: _description_

    Returns:
        str: _description_
    """
    id = uuid4()
    return str(id)


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

    def create_session(self, email) -> str:
        """
            Find the user with email ->
            Generate UUID and store in db
            as the session_id
        """
        try:
            user = self._db.find_user_by(email=email)
            uuid = _generate_uuid()
            user.session_id = uuid
            self._db._session.commit()
            return uuid
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id):
        """
        Returns user from based from session_id

        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int):
        """
        destroys session
        """
        try:
            user = self._db.find_user_by(id=user_id)
            user.id = None
            self._db._session.commit()
            return None
        except NoResultFound:
            return None
