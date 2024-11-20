#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from typing import Callable
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import User

from user import Base


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db")
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add a new user to the database.

        Args:
            email (str): The user's email address.
            hashed_password (str): The hashed password for the user.

        Returns:
            User: The created User object.
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """  finds user by
            retunrs
          """
        if not kwargs:
            raise InvalidRequestError
        try:
            query = self._session.query(User).filter_by(**kwargs).first()
            if not query:
                raise NoResultFound
            return query
        except AttributeError:
            raise InvalidRequestError

    def update_user(self, user_id: int, **kwargs):
        """ find_user
            updates user information
        """
        user = self.find_user_by(id=user_id)
        for attr, value in kwargs.items():
            if not hasattr(user, attr):
                raise ValueError
            setattr(user, attr, value)
        self._session.commit()
