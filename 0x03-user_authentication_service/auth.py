#!/usr/bin/env python3
"""Module to define a method that take password and retun bytes"""
import bcrypt
from db import DB
from typing import TypeVag
from sqlalchemy.orm.exc import NoResultFound
from user import User
import uuid


class Auth:
    """A class to interact with authentication db"""

    def __init__(self):
        self._db = DB()

    def _hash_password(password: str) -> bytes:
        """Function to generate a salt to turn the input args into bytes"""
        salt = bcrypt.gensalt()
        hash_pwd = bcrypt.hashpw(password.encode('utf-8'), salt)

        return hash_pwd

    def register_user(self, email: str, password: str) -> User:
        """Function to register a new user with email and password"""
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError(f'User {email} already exists')

        hash_pwd = self._hash_password(password)

        n_user = User(email, hash_pwd)
        self._db.save_user(n_user)

        return n_user

    def valid_login(self, email: str, password: str) -> bool:
        """Function to validate login credentials
        Args:
            email (str): The user email
            password (str): The user password
        Returns:
            bool: True if login is valid, False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        if user and bcrypt.checkpw(password.encode('utf-8'),
                                   user.hashed_password):
            return True
        return False

    def _generate_uuid() -> str:
        """Function to generate a new UUID and string representation"""
        return str(uuid.uuid4())
