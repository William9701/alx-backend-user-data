#!/usr/bin/env python3
"""DB module
"""
from typing import Dict, Any

from sqlalchemy import create_engine
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///b.db", echo=False)
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

    def add_user(self, email: str, hashed_password: bytes) -> User:
        """This is the add user method"""
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.flush()  # flush the changes to the database
        self._session.refresh(new_user)  # refresh the user instance
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs: Dict[str, Any]) -> User:
        """This method takes in arbitrary keyword arguments and returns
        the first row found in the users table as filtered by the
        method’s input arguments"""
        try:
            # Construct the query dynamically based on kwargs
            query = self._session.query(User).filter_by(**kwargs)

            # Get the first result or raise NoResultFound
            user_instance = query.one()

            return user_instance

        except NoResultFound:
            # If no results are found, raise NoResultFound
            raise NoResultFound("No user found with the given criteria.")

        except InvalidRequestError as e:
            # If there is an invalid request error, raise it with a
            # meaningful message
            raise InvalidRequestError(f"Invalid request: {str(e)}")

    def update_user(self, user_id: int, **kwargs: Dict[str, Any]) -> None:
        """This is a method that takes as argument a required user_id
        integer and arbitrary keyword arguments, and returns None"""
        user = self.find_user_by(id=user_id)
        if kwargs:
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
                else:
                    raise ValueError(f"Invalid attribute: {key}")

        # Commit changes to the database
        self._session.commit()
