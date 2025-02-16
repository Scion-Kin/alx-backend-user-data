#!/usr/bin/env python3
''' Session authentication with expiration module for the API. '''

from flask import request
from datetime import datetime, timedelta
from .session_auth import SessionAuth
from os import getenv


class SessionExpAuth(SessionAuth):
    ''' Class responsible for authentication '''

    def __init__(self) -> None:
        ''' Initializes a new SessionExpAuth instance. '''

        super().__init__()
        try:
            self.session_duration = int(getenv('SESSION_DURATION', '0'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        ''' Creates a session id for the user. '''

        session_id = super().create_session(user_id)
        if type(session_id) is not str:
            return None

        self.user_id_by_session_id[session_id] = {'user_id': user_id,
                                                  'created_at': datetime.now()}
        return session_id

    def user_id_for_session_id(self, session_id=None) -> str:
        ''' Retrieves the user id of the user associated with
        a given session id. '''

        if session_id in self.user_id_by_session_id:
            session_dict = self.user_id_by_session_id[session_id]
            if self.session_duration <= 0:
                return session_dict['user_id']
            if 'created_at' not in session_dict:
                return None

            now = datetime.now()
            time_span = timedelta(seconds=self.session_duration)
            exp_time = session_dict['created_at'] + time_span
            if exp_time < now:
                return None
            return session_dict['user_id']
