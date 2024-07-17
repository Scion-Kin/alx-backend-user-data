#!/usr/bin/env python3
''' Defines a function '''

from bcrypt import hashpw, gensalt


def _hash_password(password: str) -> bytes:
    ''' Hashes a password and returns the hashed value '''

    return hashpw(password.encode('utf-8'), gensalt())
