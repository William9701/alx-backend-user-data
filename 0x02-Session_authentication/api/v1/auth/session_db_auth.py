#!/usr/bin/env python3
""" Module of session_exp_auth
"""

from .session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """class"""

    def create_session(self, user_id=None):
        """
        Create a new session for the given user.

        :param user_id: User ID for whom the session is created
        :type user_id: str or None
        :return: Session ID if successful, otherwise None
        :rtype: str or None
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieve the user ID associated with the given session ID.

        :param session_id: Session ID to lookup user ID
        :type session_id: str or None
        :return: User ID if session is found, otherwise None
        :rtype: str or None
        """
        user_session = UserSession.search({'session_id': session_id})
        if user_session:
            return user_session[0].user_id
        return None

    def destroy_session(self, request=None):
        """
        Destroy the session associated with the given request.

        :param request: Flask request object
        :type request: flask.Request or None
        :return: True if session is destroyed, otherwise False
        :rtype: bool
        """
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_session = UserSession.search({'session_id': session_id})
        if user_session:
            user_session[0].remove()
            return True
        return False
