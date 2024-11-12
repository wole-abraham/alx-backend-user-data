#!/usr/bin/env python3
""" basic_authentication module"""
from api.v1.auth.auth import Auth
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
