#!/usr/bin/env python3
''' This defines functions '''

from bcrypt import gensalt, hashpw, checkpw


def hash_password(password: str) -> bytes:
    ''' returns a hashed password '''

    return hashpw(password.encode('utf-8'), gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    ''' checks if a password matches the hashed password '''

    return checkpw(password.encode('utf-8'), hashed_password)
