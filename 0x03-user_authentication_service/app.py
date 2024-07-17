#!/usr/bin/env python3
''' This contains a flask application '''

from flask import Flask, jsonify, request, abort, make_response, redirect
from auth import Auth

AUTH = Auth()
app = Flask(__name__)


@app.route('/')
def home():
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users():

    email, password = request.form.get('email'), request.form.get('password')
    if not email or not password:
        return jsonify()

    try:
        AUTH.register_user(email, password)
        return jsonify({"email": f"{email}", "message": "user created"})

    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login():
    ''' Creates a new user session (Logs a user in) '''

    email, password = request.form.get('email'), request.form.get('password')
    if not email or not password or not AUTH.valid_login(email, password):
        abort(401)

    resp = make_response(jsonify({"email": f"{email}",
                                  "message": "logged in"}))
    resp.set_cookie("session_id", AUTH.create_session(email))

    return resp


@app.route('/sessions', methods=['DELETE'])
def logout():
    ''' Deletes a user session (Logs out the user) '''

    session_id = request.cookies.get('session_id')

    if session_id is None:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)

    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile')
def profile():
    ''' Gets a user's profile '''

    session_id = request.cookies.get('session_id')

    if session_id is None:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)

    return jsonify({"email": f"{user.email}"})


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    ''' Returns a user's password reset token '''

    email = request.form.get('email')

    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": f"{email}", "reset_token": f"{token}"})

    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['PUT'])
def update_password():
    ''' Updates a user's password'''

    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')

    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"})

    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
