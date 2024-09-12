#!/usr/bin/env python3
"""Auth module
"""
import bcrypt
import uuid
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
            user_p = user.hashed_password
            input_p_b = password.encode('utf-8')
            if not bcrypt.checkpw(input_p_b, user_p):
                return False
            return True
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """ a function that takes an email string argument
        and returns the session ID as a string
        """
        if not isinstance(email, str):
            return None

        # find the user
        try:
            user = self._db.find_user_by(email=email)
            session_id = str(uuid.uuid4())
            update_dict = {
                "session_id": session_id
            }
            self._db.update_user(user.id, **update_dict)
            return session_id
        except NoResultFound:
            """if the block that calls this function checks for a value
            error then I should raise a valueerror at this point
            """
            return

    def get_user_from_session_id(self, session_id: str) -> str:
        """a function to get a user from a session id"""
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: str) -> None:
        """
        Function to destroy a session using the id of the user

        Params:
        user_id: the id of the user

        Returns:
        returns None
        """
        self._db.update_user(user_id, session_id=None)

        return None


def _hash_password(password: str) -> str:
    """returns a hashed password"""
    if not isinstance(password, str):
        return
    return (
        bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        )
    )


def _generate_uuid() -> str:
    """a function to generate a uuid using the
    uuid module
    """
    return str(uuid.uuid4())
