#!/usr/bin/env python3
"""Flask app"""
from flask import Flask, jsonify, url_for, request, abort, redirect
from auth import Auth

AUTH = Auth()


app = Flask(__name__)


@app.route('/', methods=["GET"])
def home() -> str:
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


@app.route('/sessions', methods=['DELETE'])
def logout() -> str:
    """
    Route: /sessions
    Methods: 'DELETE'

    Return:
    Redirects user if the user exist
    403 Status if Not
    """
    session_id = request.cookies.get('session_id')
    if not session_id:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    AUTH.destroy_session(user.id)

    return redirect(url_for('home'))


@app.route('/profile', methods=['GET'])
def profile() -> str:
    """
    returns a user profile
    Request:
    must have a session_id cookie
    Return:
    if the user exists, respond with a 200 status
    and the following JSON payload
    {"email": "<user email>"}
    """
    session_id = request.cookie.get('session_id')
    if not session_id:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)

    payload = jsonify(
        {
            "email": user.email
        }
    )
    return payload


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
