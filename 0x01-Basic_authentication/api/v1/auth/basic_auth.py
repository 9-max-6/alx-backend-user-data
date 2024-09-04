#!/usr/bin/env python3
"""Basic auth module"""
import base64
import binascii
from typing import Tuple, TypeVar
from api.v1.auth.auth import Auth
from models.user import User


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

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str
            ) -> Tuple[str, str]:
        """A function to extract the user credentials"""
        delimeter = ":"
        user_email = ""
        user_password = ""
        split_string = []

        if not decoded_base64_authorization_header:
            return None
        if type(decoded_base64_authorization_header) is not str:
            return None

        if delimeter not in decoded_base64_authorization_header:
            return None

        split_string = decoded_base64_authorization_header.split(delimeter)
        user_email, user_password = split_string

        return (user_email, user_password)

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str
            ) -> TypeVar('User'):
        """
        Fetch user instance
        This function returns the User instance based on the email and password
        Parameters:
        user_email(str) - the email of the user to lookup
        user_pwd(str) - the password of the user to lookup

        Returns:None if the user_email or user_pwd is None
                None if the database doesn't contain a User with that email
                None if the password is invalid
                The User is authentication was successful.
        """

        if type(user_email) == str and type(user_pwd) == str:
            try:
                users = User.search({'email': user_email})
            except Exception:
                return None
            if len(users) <= 0:
                return None
            if users[0].is_valid_password(user_pwd):
                return users[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieves the current user from a request.
        """
        auth_header = self.authorization_header(request)
        b64_auth_token = self.extract_base64_authorization_header(auth_header)
        auth_token = self.decode_base64_authorization_header(b64_auth_token)
        email, password = self.extract_user_credentials(auth_token)
        return self.user_object_from_credentials(email, password)
