#!/usr/bin/env python3
""" Module of auth
"""
from flask import request
from typing import List, TypeVar
from os import getenv


class Auth:
    """ Authentication class """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """returns False"""
        if path is None or len(path) == 0:
            return True
        elif excluded_paths is None or len(excluded_paths) == 0:
            return True
        elif path:
            if path[-1] != '/':
                path = path + '/'
            if path in excluded_paths:
                return False
            else:
                return True

    def authorization_header(self, request=None) -> str:
        """ returns False """
        if request is None or request.headers.get('Authorization') is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """ return False """
        return None

    def session_cookie(self, request=None):
        """ returns cookie value """
        if request is None:
            return None
        return request.cookies.get(getenv('SESSION_NAME'))
