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


@app_views.route("/auth_session/login", methods=['POST'], strict_slashes=False)
def auth_session():
    email = request.form.get('email')
    passsword = request.form.get("password")
    if email is None:
        return jsonify({"error": "email missing"}), 400
    if passsword is None:
        return jsonify({"error": "password missing"}), 400

    user = User.search({"email": email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404
    if not user[0].is_valid_password(passsword):
        return jsonify({"error": "wrong password"}), 404
    else:
        from api.v1.app import auth
        key = auth.create_session(user[0].id)
        out = jsonify(user[0].to_json())
        out.set_cookie(getenv("SESSION_NAME"), key)
        return out
