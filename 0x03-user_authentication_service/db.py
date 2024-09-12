#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine, tuple_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from typing import TypeVar, Any
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db")
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
        """
        function to add a new user
        """
        try:
            user = User(email=email, hashed_password=hashed_password)
            self._session.add(user)
            self._session.commit()
        except Exception:
            self._session.rollback()
            user = None
        return user

    def find_user_by(self, **kwargs: dict[str, Any]) -> User:
        """A function to find a user using an attrbute"""
        cols = []
        values = []
        for col, val in kwargs.items():
            if hasattr(User, col):
                cols.append(getattr(User, col))
                values.append(val)
            else:
                raise InvalidRequestError()

        grouped_columns = tuple_(*cols)
        result = self._session.query(User).filter(
            grouped_columns.in_([tuple(values)])
        ).first()

        if not result:
            raise NoResultFound()
        return result
