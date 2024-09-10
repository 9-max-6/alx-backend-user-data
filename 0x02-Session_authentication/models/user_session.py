#!/usr/bin/env python3
""" Session storage
"""
from models.base import Base

class UserSession(Base):
    """class to implement session storage logic"""

    def __init__(self, *args: list, **kwargs: dict):
        """init"""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
