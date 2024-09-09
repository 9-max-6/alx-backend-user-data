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
        if not excluded_paths or len(excluded_paths) == 0:
            return True

        trimmed_paths = []
        paths_with_asterisk = []
        for pathe in excluded_paths:
            if not pathe.endswith('/'):
                if not pathe.endswith('*'):
                    pathe += '/'
            trimmed_paths.append(pathe)

            if pathe.endswith('*'):
                paths_with_asterisk.append(pathe)

        if not path.endswith('/'):
            path += '/'

        if path in trimmed_paths:
            return False

        if len(paths_with_asterisk) == 0:
            return True

        found = False
        for pathh in paths_with_asterisk:
            if path[:len(pathh) - 1] in pathh:
                found = True
        return found

    def authorization_header(self, request=None) -> str:
        """returns None"""
        if not request:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """a function that returns None"""
        return None
