#!/usr/bin/env python3
''' This defines a class '''

from flask import request
from .auth import Auth
from models.user import User
from uuid import uuid4


class SessionAuth(Auth):
    ''' Class responsible for authentication '''

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        ''' creates a session for a user_id '''

        if user_id is None or type(user_id) is not str:
            return None

        ses_id = str(uuid4())
        SessionAuth.user_id_by_session_id[ses_id] = user_id

        return ses_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        ''' returns a User ID associated with a Session ID '''

        return SessionAuth.user_id_by_session_id.get(session_id, None)

    def current_user(self, request=None):
        ''' returns a User instance based on a cookie value '''

        u_id = self.user_id_for_session_id(self.session_cookie(request))

        return User.get(u_id)

    def destroy_session(self, request=None):
        ''' deletes the user session (logs out) '''

        sess_id = self.session_cookie(request)
        if request is None or sess_id is None:
            return False

        if sess_id not in self.user_id_by_session_id:
            return False

        del self.user_id_by_session_id[sess_id]
        return True
