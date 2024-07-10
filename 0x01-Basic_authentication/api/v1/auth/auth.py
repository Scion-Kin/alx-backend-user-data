#!/usr/bin/env python3
''' This defines a class '''

from flask import request
from typing import List, TypeVar


class Auth:
    ''' Class responsible for authentication '''

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        ''' Checks if the requested path is in the excluded paths '''

        return False

    def authorization_header(self, request=None) -> str:
        ''' checks for an auth token in the request's header '''

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        ''' verifies the user '''

        return None
