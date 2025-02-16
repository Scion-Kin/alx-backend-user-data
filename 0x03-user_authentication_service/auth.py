#!/usr/bin/env python3
''' Defines a function '''

from bcrypt import hashpw, gensalt, checkpw
from db import DB
from user import User
from uuid import uuid4
from sqlalchemy.orm.exc import NoResultFound
from typing import Union


def _hash_password(password: str) -> bytes:
    ''' Hashes a password and returns the hashed value '''

    return hashpw(password.encode('utf-8'), gensalt())


def _generate_uuid() -> str:
    ''' returns a uuid '''

    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        ''' makes and stores a new User object '''

        try:
            self._db.find_user_by(email=email)

        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))

        raise ValueError('User {} already exists'.format(email))

    def valid_login(self, email: str, password: str) -> bool:
        ''' Checks if the given password is the valid registered one '''

        try:
            user = self._db.find_user_by(email=email)
            return checkpw(password.encode('utf-8'), user.hashed_password)

        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        ''' Creates a session ID and stores it in the database '''

        try:
            user = self._db.find_user_by(email=email)
            user.session_id = _generate_uuid()

            self._db._session.commit()
            return user.session_id

        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        ''' Find a user object associated with a session ID '''

        try:
            return self._db.find_user_by(session_id=session_id)

        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        ''' deletes the session id from a User object '''

        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        ''' sets a reset token on a user object '''

        try:
            user, token = self._db.find_user_by(email=email), _generate_uuid()

            self._db.update_user(user.id, reset_token=token)
            return token

        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        ''' Updates a user's password '''

        try:
            user = self._db.find_user_by(reset_token=reset_token)
            self._db.update_user(user.id,
                                 hashed_password=_hash_password(password),
                                 reset_token=None)

        except NoResultFound:
            raise ValueError
