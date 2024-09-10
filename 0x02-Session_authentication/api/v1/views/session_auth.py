#!/usr/bin/env python3
""" Module of Index views
"""
import os
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.user import User
from api.v1.app import auth


@app_views.route(
        '/auth_session/login',
        methods=['POST'],
        strict_slashes=False
        )
def login() -> str:
    """a function to implement login logic"""
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return ({
            "error": "email missing"
        }), 400

    if not password:
        return jsonify(
            {
                "error": "password missing"
            }
        ), 400

    user = User.search({"email": email})
    if not user:
        return jsonify(
            {
                "error": "no user found for this email"
            }
        ), 404

    if not user[0].is_valid_password(password):
        return jsonify(
            {
                "error": "wrong password"
            }
        ), 401

    from api.v1.app import auth
    session_id = auth.create_session(user[0].id)
    cookie_name = os.getenv("SESSION_NAME")
    if cookie_name:
        resp = jsonify(user[0].to_json())
        resp.set_cookie(cookie_name, session_id)
        return resp


@app_views.route(
    '/auth_session/logout',
    methods=['DELETE'],
    strict_slashes=False
)
def logout() -> str:
    """a function to implement logout logic"""
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
