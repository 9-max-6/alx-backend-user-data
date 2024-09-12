#!/usr/bin/env python3
"""Flask app"""
from flask import Flask, jsonify, request, abort
from auth import Auth

AUTH = Auth()


app = Flask(__name__)


@app.route('/', methods=["GET"])
def hello() -> str:
    """simple hello route"""
    return jsonify(
        {
            "message": "Bienvenue"
        }
    )


@app.route('/users', methods=["POST"])
def users() -> str:
    """registers a user"""
    email = request.form.get('email')
    password = request.form.get('password')

    if not email and not password:
        pass
    try:
        AUTH.register_user(email, password)
        return jsonify(
            {"email": email, "message": "user created"}
        )
    except ValueError:
        return jsonify(
            {"message": "email already registered"}
        ), 400


@app.route('/sessions', methods=["POST"])
def login() -> str:
    """a function to implement the login login"""
    email = request.form.get('email')
    password = request.form.get('password')

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)
    payload = {"email": email,
               "message": "logged in"
               }
    response = jsonify(payload)
    response.set_cookie("session_id", session_id)

    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
