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
        return str(uuid4())

    def create_session(self, email: str) -> str:
        """Function to create session for user and return the session ID
        Args:
            email (str): The email of the user
        Returns:
            str: The session ID as a string.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        session_id = self._generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str):
        """Function to get a user from a session ID
        Args:
            session_id (str): The session ID
        Returns:
            User: The user object or None
        """
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Function to destroy session by setting the user's
        session ID to None
        Args:
            user_id (int): The user ID
        Returns:
            None
        """
        self._db.update_user(user_id, session_id=None)
