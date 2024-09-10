#!/usr/bin/env python3
"""Session expiration logic"""
import os
from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """a class to implement session logic"""

    def __init__(self):
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION', 0))
        except Exception as e:
            self.session_duration = 0

    def create_session(self, user_id: str = None) -> str:
        """function to create a session"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None

        SessionAuth.user_id_by_session_id[session_id] = {
                "user_id": user_id,
                "created_at": datetime.now()
            }

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """a function to overload user_id_for session"""
        if not session_id:
            return None
        if not hasattr(SessionAuth.user_id_for_session_id, session_id):
            return None
        session_dictionary = SessionExpAuth.user_id_by_session_id.get(
                session_id
        )

        if self.session_duration <= 0:
            return session_dictionary.get(
                "user_id"
            )

        created_at = session_dictionary.get("created_at")
        if not created_at:
            return None

        now = datetime.now()
        session_time = created_at + timedelta(self.session_duration)

        if session_time < now:
            return None
        return session_dictionary.get(
                "user_id"
            )
