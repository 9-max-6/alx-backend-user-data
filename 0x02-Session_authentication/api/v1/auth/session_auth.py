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

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """a function to return user_id for a session id"""
        if not session_id:
            return None
        if not isinstance(session_id, str):
            return None
        return SessionAuth.user_id_for_session_id.get(
            session_id
        )
