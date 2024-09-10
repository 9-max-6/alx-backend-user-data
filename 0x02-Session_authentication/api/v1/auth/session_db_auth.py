#!/usr/bin/env python3
"""Session db-storage logic"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession 


class SessionDBAuth(SessionExpAuth):
    """ session DB """

    def create_session(self, user_id: str = None) -> str:
        """create session overload"""
        session_id = super().create_session(user_id)
        
        if not session_id:
            return None
        
        user_session = {
        "session_id": session_id,
        "user_id": user_id
        }
        session = UserSession(**user_session)
        session.save()
    
    def user_id_for_session_id(self, session_id: str = None) -> str:
        """function to fetch user id from the database based on session_id"""
        if not session_id:
            return
        session = UserSession.search({
            "session_id": session_id
        })
        if not session:
            return
        return session.user_id

    def destroy_session(self, request=None):
        """a function to destroy session"""
        cookie = self.session_cookie(request)
        
