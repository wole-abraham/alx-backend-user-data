#!/usr/bin/env python3
""" Module of auth
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """ Authentication class """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """returns False"""
        return False

    def authorization_header(self, request=None) -> str:
        """ returns False """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ return False """
        return None
