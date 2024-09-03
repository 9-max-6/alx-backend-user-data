#!/usr/bin/env python3
"""Basic auth module"""
from api.v1.auth.auth import Auth


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
        if not authorization_header.startswith(prefix):
            return None
        return authorization_header[len(prefix):]
