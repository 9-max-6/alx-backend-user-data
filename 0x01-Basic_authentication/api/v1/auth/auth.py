#!/usr/bin/env python3
"""Auth module"""
from flask import request
from typing import List, TypeVar
from models.user import User


class Auth:
    """a class to wrap auth logic"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> str:
        """a function that returns False"""
        if not path:
            return True
        if len(excluded_paths) == 0 or not excluded_paths:
            return True
        if path[-1] != '/':
            path = path + '/'
        if path in excluded_paths:
            return False
        else:
            return True

    def authorization_header(self, request=None) -> str:
        """returns None"""

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """a function that returns None"""
        return None
