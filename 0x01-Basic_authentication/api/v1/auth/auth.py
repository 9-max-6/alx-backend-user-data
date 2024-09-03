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

        trimmed_paths = []
        for pathe in excluded_paths:
            if not pathe.endswith('/'):
                pathe += '/'
            trimmed_paths.append(pathe)

        if not path.endswith('/'):
            path += '/'

        if path in trimmed_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """returns None"""
        if not request:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """a function that returns None"""
        return None


class BasicAuth(Auth):
    """Empty class"""
    def extract_base64_authorization_header(
            self,
            authorization_header: str
            ) -> str:
        """returns the Base64 part of the Authorization
        header for a Basic Authentication:
        """
        if not authorization_header:
            return None
        if not isinstance(authorization_header, str):
            return None
        prefix = 'Basic '
        if not authorization_header.startswith(
            prefix
            ):
            return None
        return authorization_header[len(prefix):]
