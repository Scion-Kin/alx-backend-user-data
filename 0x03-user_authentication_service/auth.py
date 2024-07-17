#!/usr/bin/env python3
''' Defines a function '''

from bcrypt import hashpw, gensalt
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    ''' Hashes a password and returns the hashed value '''

    return hashpw(password.encode('utf-8'), gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        ''' makes and stores a new User object '''

        try:
            user = self._db.find_user_by(email=email)
            raise ValueError('User {} already exists'.format(email))

        except ValueError:
            raise

        except Exception:
            user = User(email=email, hashed_password=_hash_password(password))

            self._db._session.add(user), self._db._session.commit()
            return
