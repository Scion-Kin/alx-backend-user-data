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
def logout() -> str:
    ''' Deletes a user session (Logs out the user) '''

    session_id = request.cookies.get('session_id')

    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)

    AUTH.destroy_session(user.id)
    return redirect('/')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
