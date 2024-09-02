"""Auth module"""
from flask import request
from typing import List, TypeVar
from models.user import User

class Auth:
    """a class to wrap auth logic"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> str:
        """a function that returns False"""
        return False

    def authorization_header(self, request=None) -> str:
        """returns None"""

        return None
    
    def current_user(self, request=None) -> TypeVar('User'):
        """a function that returns None"""
        return None