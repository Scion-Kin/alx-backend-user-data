#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth
from api.v1.auth.session_db_auth import SessionDBAuth
from api.v1.auth.session_exp_auth import SessionExpAuth
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth_type = getenv('AUTH_TYPE', 'auth')

auths = {"auth": Auth(), "basic_auth": BasicAuth(),
         "session_auth": SessionAuth(),
         "session_exp_auth": SessionExpAuth(),
         "session_db_auth": SessionDBAuth()}

auth = auths.get(auth_type)


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    ''' Unauthorized '''

    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    ''' The error handler for a forbidden request '''

    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def before_req():
    ''' Handle the request '''
    if auth:
        excluded_paths = ['/api/v1/status/',
                          '/api/v1/unauthorized/',
                          '/api/v1/forbidden/',
                          '/api/v1/auth_session/login/']

        if auth.require_auth(request.path, excluded_paths):
            user = auth.current_user(request)

            if auth.authorization_header(request) is None and\
                    auth.session_cookie(request) is None:
                abort(401)

            if user is None:
                abort(403)

            request.current_user = user


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
