#!/usr/bin/env python3
"""
auth file
"""

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password: str) -> bytes:
    """ hash a password"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)


def _generate_uuid() -> str:
    """Generate a new UUID."""
    new_uuid = uuid.uuid4()
    return str(new_uuid)


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """the init class"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """register a user"""
        try:
            existing_user = self._db.find_user_by(email=email)
            raise ValueError(f"User {existing_user.email} already exists.")
        except NoResultFound:
            # If NoResultFound is raised, it means the user doesn't exist,
            # so proceed with registration.
            pass
        if isinstance(password, str):
            password = _hash_password(password)

        return self._db.add_user(email=email, hashed_password=password)

    def valid_login(self, email: str, password: str) -> bool:
        """Validates login details."""
        try:
            existing_user = self._db.find_user_by(email=email)
            hashed_password_bytes = existing_user.hashed_password

            if bcrypt.checkpw(password.encode('utf-8'),
                              hashed_password_bytes):
                return True
            return False
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """this method  takes an email string argument and returns the
        session ID as a string"""
        try:
            user = self._db.find_user_by(email=email)
            session_uuid = _generate_uuid()
            self._db.update_user(user.id, session_id=session_uuid)
            return session_uuid
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """destroys a session"""
        try:
            self._db.update_user(user_id, session_id=None)
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User or None:
        """this method  takes a single session_id string argument and
        returns the corresponding User or None"""
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """gets to reset the password"""
        try:
            user = self._db.find_user_by(email=email)
            uu_id = _generate_uuid()
            self._db.update_user(user.id, reset_token=uu_id)
            return uu_id
        except NoResultFound:
            raise ValueError('User does not exist')

    def update_password(self, reset_token: str, password: str) -> None:
        """Update password"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_pwd = _hash_password(password)
            self._db.update_user(user.id, hashed_password=hashed_pwd,
                                 reset_token=None)
        except NoResultFound:
            raise ValueError('user not found')
