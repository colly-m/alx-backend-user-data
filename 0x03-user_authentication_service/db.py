#!/usr/bin/env python3
"""Module to implememnt the add user method"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from typing import TypeVar


from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Function to add a new user to the database
        Args:
        email (str): The email of the user
        hashed_password (str): The hashed password of the user
        Returns:
        User: The newly created User object
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """Function to find user in the database by given keyword args
        Args:
        **kwargs: keyword arguments to filter the query by
        Returns:
        User: The first User table as filtered by the method’s input args
        Raises:
        NoResultFound: When no results are found
        InvalidRequestError: When wrong query arguments are passed
        """
        try:
            outcome = self._session.query(User).filter_by(**kwargs).first()
            if outcome is None:
                raise NoResultFound
            return outcome
        except InvalidRequestError as e:
            raise InvalidRequestError

    def update_user(self, user_id: int, **kwargs) -> None:
        """Function to update a user's attributes.
        Args:
            user_id (int): user ID to update.
            **kwargs: keyword args for attributes to update
        Raises:
            ValueError: If an argument does not correspond to a user attribute.
        """
        session = self._session
        user = self.find_user_by(id=user_id)

        for key, val in kwargs.items():
            if not hasattr(user, key):
                raise ValueError
            setattr(user, key, val)

        session.commit()
