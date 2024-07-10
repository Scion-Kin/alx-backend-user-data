#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from api.v1.auth import auth
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = getenv('AUTH_TYPE', None)

if auth is not None:
    auth = Auth()


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
    if auth is None:
        pass

    else:
        path_in = auth.require_auth(request.path, ['/api/v1/status/',
                                                   '/api/v1/unauthorized/',
                                                   '/api/v1/forbidden/'])
        if not path_in:
            pass

        if auth.authorization_header(request) is None:
            abort(401)

        if auth.current_user(request) is None:
            abort(403)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port, debug=True)
