import pytest
from core.user.models import User


'''
For different model testing we need user ready so we will implement with fixtures
A fixture is a function that will run before each test function to which
it's applied 

'''
 

data_user = {
    "username": "test_user",
    "email": "test@gmail.com",
    "first_name": "Test",
    "last_name": "User",
    "password": "test_password"
}

@pytest.fixture
def user(db) -> User:
    return User.objects.create_user(**data_user)