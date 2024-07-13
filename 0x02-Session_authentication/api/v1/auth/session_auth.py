#!/usr/bin/env python3
''' This defines a class '''

from flask import request
from .auth import Auth
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
