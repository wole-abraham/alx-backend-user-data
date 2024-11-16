#!/usr/bin/env python3
""" Sessino authentication """
from api.v1.auth.auth import Auth
from os import getenv
from uuid import uuid4
from models.user import User
from api.v1.views import app_views
from flask import request, jsonify, session
from models.user import User


class SessionAuth(Auth):
    """ Session Auth
        returns the newly cerated session_id
    """

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ cretes session
            and returns session id
        """
        if user_id is None:
            return None
        if not (isinstance(user_id, str)):
            return None

        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ return the users id based in the Session ID """
        if session_id is None:
            return None
        if not (isinstance(session_id, str)):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """ returns the current user bases of the
            session id
        """
        key_to_session = self.session_cookie(request)
        user = self.user_id_for_session_id(key_to_session)
        return User.get(user)

    def destroy_session(self, request=None):
        """ destroys user sesssion """
        if request is None:
            return False
        session_cookie = self.session_cookie(request)
        if session_cookie is None:
            return False
        user_id = self.user_id_for_session_id(session_cookie)
        if user_id is None:
            return False
        del self.user_id_by_session_id[session_cookie]
        return True
