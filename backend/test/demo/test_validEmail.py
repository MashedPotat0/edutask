import pytest
import unittest.mock as mock

from src.controllers.usercontroller import UserController

@pytest.fixture

def test_hasAttribute_false():
    email = {'email': 'Jane'}
    result = UserController.get_user_by_email(email, 'sd')
    assert result == False

def test_hasAttribute_true():
    object = {'email': 'jane.doe@gmail.com'}
    mockedusercontroller = UserController
    result = UserController.get_user_by_email(mockedusercontroller, object)
    assert result == True