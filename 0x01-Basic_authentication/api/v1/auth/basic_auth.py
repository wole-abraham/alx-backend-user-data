#!/usr/bin/env python3
""" basic_authentication module"""
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar
import base64
import binascii


class BasicAuth(Auth):
    """ Basic Authentication """
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """ base64 authorization header """
        if authorization_header is None:
            return None
        if not (isinstance(authorization_header, str)):
            return None
        if authorization_header.split()[0] != 'Basic':
            return None
        else:
            return authorization_header.split()[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """ decode base64 authorizaton header  """
        if base64_authorization_header is None:
            return None
        if not (isinstance(base64_authorization_header, str)):
            return None
        try:
            decoded = base64.b64decode(base64_authorization_header)
        except binascii.Error:
            return None
        else:
            return decoded.decode()

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> str:
        """ Extract user credentials """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not (isinstance(decoded_base64_authorization_header, str)):
            return (None, None)
        if ":" not in decoded_base64_authorization_header:
            return (None, None)
        a, b = (x for x in decoded_base64_authorization_header.split(':'))
        return (a, b)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """ user object from credential """
        if user_email is None or user_pwd is None:
            return None
        if not (isinstance(user_email, str)):
            return None
        if not (isinstance(user_pwd, str)):
            return None
        user = User.search({'email': user_email})
        if len(user) == 0:
            return None
        if user[0].is_valid_password(user_pwd):
            return user[0]
        else:
            return None
