#!/usr/bin/env python3
"""Auth module
"""
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """A function to register a user"""
        try:
            if self._db.find_user_by(email=email):
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            pass
        new_user = self._db.add_user(email, _hash_password(password))
        if new_user:
            return new_user
    
    def valid_login(self, email: str, password: str) -> bool:
        """A function to validate password"""
        
        try:
            user = self._db.find_user_by(email=email)
            if not bcrypt.checkpw(
                password.encode('utf-8'),
                user.hashed_password
                ):
                return False
            return True
        except NoResultFound:
            return False

def _hash_password(password: str) -> str:
    """returns a hashed password"""
    if not isinstance(password, str):
        return
    return(
        bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        )
    )
