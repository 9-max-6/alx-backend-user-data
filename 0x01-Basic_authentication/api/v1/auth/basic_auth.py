#!/usr/bin/env python3
"""Basic auth module"""
import base64
import binascii
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

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str
            ) -> str:
        """A function to decode the Base64 string"""
        if not base64_authorization_header:
            return None
        if type(base64_authorization_header) is not str:
            return None
        try:
            decoded_data = base64.b64decode(base64_authorization_header)
            return decoded_data.decode('utf-8')
        except binascii.Error as e:
            return None
