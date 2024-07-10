#!/usr/bin/env python3
''' This defines a class '''

from flask import request
from typing import List, TypeVar


class Auth:
    ''' Class responsible for authentication '''

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        ''' Checks if the requested path is in the excluded paths '''
 
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True

        path = path + '/' if not path.endswith('/') else path

        return True if path not in excluded_paths else False

    def authorization_header(self, request=None) -> str:
        ''' checks for an auth token in the request's header '''

        auth_header = request.headers.get('Authorization')

        return None if request is None or not auth_header else auth_header

    def current_user(self, request=None) -> TypeVar('User'):
        ''' verifies the user '''

        return None
