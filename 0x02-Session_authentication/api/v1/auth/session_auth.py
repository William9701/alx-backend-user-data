#!/usr/bin/env python3
""" Module of session_auth
"""
import uuid

from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """Class SessionAuth"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ method that creates a session"""
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        Session_ID = str(uuid.uuid4())
        self.user_id_by_session_id[Session_ID] = user_id
        return Session_ID

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ a method that returns a User ID based on a Session ID"""
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> User:
        """Return a User instance based on a cookie value"""
        session_id = self.session_cookie(request)
        if session_id is None:
            return None

        user_id = self.user_id_by_session_id.get(session_id)
        if user_id is None:
            return None

        return User.get(user_id)

