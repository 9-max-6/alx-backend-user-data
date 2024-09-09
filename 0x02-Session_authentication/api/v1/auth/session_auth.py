#!/usr/bin/env python3
"""Session authentication logic"""
import uuid
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """
    Session class
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """a function to create a session ID for a user_id"""
        if not user_id:
            return None
        if not isinstance(user_id, str):
            return None
        session_id = uuid.uuid4()
        SessionAuth.user_id_by_session_id[session_id] = user_id

        return session_id
