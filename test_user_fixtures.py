from faker import Faker

fake = Faker()

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


import pytest
import ipytest # in order to use pytest in jupyter notebook

@pytest.fixture
def user():
    """
    Create user with random username, password, email, using fake
    """
    return User(username=fake.name(), password=fake.password(), 
               email=fake.email())


def test_user(user):
    print(f"Fake user is: {user}")