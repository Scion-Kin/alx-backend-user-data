#!/usr/bin/env python3
''' This defines a class '''

from flask import request
from .auth import Auth


class SessionAuth(Auth):
    ''' Class responsible for authentication '''
