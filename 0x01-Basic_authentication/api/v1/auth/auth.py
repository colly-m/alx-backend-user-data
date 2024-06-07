#!/usr/bin/env python3
"""Module to define a class auth"""
from flask import request
from typing import List, TypeVar


User = TypeVar('User')


class Auth:
    """Class fo manage API authentifications"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        if path is None:
            return True
        if excluded_paths is None or not excluded_paths:
            return True

        if not path.endswith('/'):
            path += '/'

        for excluded_path in excluded_paths:
            if not excluded_path.endswith('/'):
                excluded_path += '/'
            if path == excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """"Function to check for authorized header"""
        key = 'Authorization'

        if request is None or key not is request.headers:
            return
        return request.headers.get(key)


    def current_user(self, request=None) -> User:
        """Function to return None on request"""
        return None
