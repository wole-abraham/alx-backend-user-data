#!/usr/bin/env python3
""" hashed passwords using bcrypt"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """
    password_string -> hashed_password
    bcrypt.hashpw
    """
    salt = bcrypt.gensalt()
    password = password.encode('utf-8')
    hash = bcrypt.hashpw(password, salt)
    return hash
