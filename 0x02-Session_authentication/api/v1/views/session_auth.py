#!/usr/bin/env python3
''' Defines session authentication routes '''

from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    ''' Authenticates a user '''
    from api.v1.app import auth

    email, password = request.form.get('email'), request.form.get('password')

    if email is None:
        return jsonify({"error": "email missing"}), 400

    if password is None:
        return jsonify({"error": "password missing"}), 400

    items = User.search({"email": email})
    if len(items) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    if not items[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    sess_id = auth.create_session(items[0].id)
    resp = make_response(jsonify(items[0].to_json()))
    resp.set_cookie(getenv('SESSION_NAME'), sess_id)

    return resp
