#!/usr/bin/env python3
""" Sessino authentication """
from api.v1.auth.auth import Auth
from uuid import uuid4


class SessionAuth(Auth):
    """ Session Auth
        returns the newly cerated session_id
    """

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        if user_id is None:
            return None
        if not (isinstance(user_id, str)):
            return None

        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id
