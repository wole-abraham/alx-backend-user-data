#!/usr/bin/env python3
""" basic_authentication module"""
from api.v1.auth.auth import Auth


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
