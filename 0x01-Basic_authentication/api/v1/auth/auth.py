#!/usr/bin/env python3
""" Module of auth
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """ Authentication class """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """returns False"""
        if path is None:
            return True
        elif excluded_paths is None:
            return True
        elif path:
            if path[-1] != '/':
                path = path + '/'
            if path in excluded_paths:
                return False

    def authorization_header(self, request=None) -> str:
        """ returns False """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ return False """
        return None
