#!/usr/bin/env python3
"""This is the basicauth module"""
import base64
from typing import TypeVar

from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    """ class Basic auth"""

    def extract_base64_authorization_header(self,
                                            authorization_header:
                                            str) -> str:
        """extract base64 """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str
    ) -> str:
        """Decode a Base64 string"""
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            base64_bytes = base64_authorization_header.encode('utf-8')
            message_bytes = base64.b64decode(base64_bytes)
            return message_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> (
            str, str):
        """Extract user credentials from Base64 string"""
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None

        credentials = decoded_base64_authorization_header.split(':', 1)
        return credentials[0], credentials[1]

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """Return User instance based on email and password"""
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            users = User.search({'email': user_email})
        except Exception:
            return None

        for user in users:
            if user.is_valid_password(user_pwd):
                return user

        return None

    def current_user(self, request=None) -> User:
        """
        Retrieve the User instance for a request.

        :param request: Flask request object
        :type request: flask.Request or None
        :return: User instance or None if request is None
        :rtype: User or None
        """
        if request is None:
            return None

        authorization_header = self.authorization_header(request)
        base64_authorization_header = (
            self.extract_base64_authorization_header(authorization_header)
        )
        decoded_base64_authorization_header = (
            self.decode_base64_authorization_header(
                base64_authorization_header)
        )
        user_email, user_pwd = self.extract_user_credentials(
            decoded_base64_authorization_header
        )

        return self.user_object_from_credentials(user_email, user_pwd)
