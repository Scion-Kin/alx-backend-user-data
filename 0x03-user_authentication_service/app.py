#!/usr/bin/env python3
''' This contains a flask application '''

from flask import Flask, jsonify, request
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
