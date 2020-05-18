from faker import Faker

class User:
    """
    Class for representing a user in our application
    """

    def __init__(self, username: str, email: str, password: str):
        self.__username = username
        self.__email = email
        self.__password = password

    ### @property -> getter
    @property
    def username(self) -> str:
        return self.__username

    @property
    def email(self) -> str:
        return self.__email

    @property
    def password(self) -> str:
        return self.__password

    ### @attribute -> setter
    @username.setter
    def username(self, val: str):
        self.__username = val

    @password.setter
    def password(self, val: str):
        self.__password = val

    @email.setter
    def email(self, val: str):
        self.__email = val

    def __str__(self):
        return f"Username: {self.__username} - Password: {self.__password} - Email: {self.email}\n"


fake = Faker()

import pytest
import ipytest # in order to use pytest in jupyter notebook

@pytest.fixture
def user_invalid_name():
    """
    Create user with random password, email, and invalid name using fake
    """
    return User(username=".p123axzc~wqq ", password=fake.password(), 
               email=fake.email())


def is_username_valid(username: str):
    for char in username:
        if char in "?~ -":
            return False
    
    return True

def test_user_invalid_name(user_invalid_name):
    username = user_invalid_name.username

    assert is_username_valid(username) is False    