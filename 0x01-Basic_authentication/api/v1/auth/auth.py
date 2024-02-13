#!/usr/bin/env python3
"""this is the auth class"""
import fnmatch

from flask import request

from typing import List, TypeVar


class Auth:
    """This is the Auth class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Returns True if the path is not in the list of strings excluded_paths"""
        if path is None:
            return True

        if excluded_paths is None or not excluded_paths:
            return True

        # Normalize paths to have a trailing slash
        normalized_path = path.rstrip("/") + "/"

        for excluded_path in excluded_paths:
            normalized_excluded_path = excluded_path.rstrip("/") + "/"
            if fnmatch.fnmatch(normalized_path, normalized_excluded_path):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """this is the auth_header"""
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """current user"""
        return None
