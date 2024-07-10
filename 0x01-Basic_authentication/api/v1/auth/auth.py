#!/usr/bin/env python3
''' This defines a class '''

from flask import request
from typing import List, TypeVar


class Auth:
    ''' Class responsible for authentication '''

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        ''' Checks if the requested path is in the excluded paths '''

        if path is not None and excluded_paths is not None:
            for exclusion_path in map(lambda x: x.strip(), excluded_paths):
                pattern = ''
                if exclusion_path[-1] == '*':
                    pattern = '{}.*'.format(exclusion_path[0:-1])
                elif exclusion_path[-1] == '/':
                    pattern = '{}/*'.format(exclusion_path[0:-1])
                else:
                    pattern = '{}/*'.format(exclusion_path)
                if re.match(pattern, path):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        ''' checks for an auth token in the request's header '''

        auth_header = request.headers.get('Authorization')

        return None if request is None or not auth_header else auth_header

    def current_user(self, request=None) -> TypeVar('User'):
        ''' verifies the user '''

        return None
