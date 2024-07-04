#!/usr/bin/env python3
''' This defines functions '''

from bcrypt import gensalt, hashpw


def hash_password(password: str) -> bytes:
    ''' returns a hashed password '''

    return hashpw(password.encode('utf-8'), gensalt())
