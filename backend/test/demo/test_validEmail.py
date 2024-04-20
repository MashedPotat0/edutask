import pytest
import unittest.mock as mock

from src.util.helpers import ValidationHelper
from src.controllers.usercontroller import UserController

@pytest.fixture
def sut():
    mockedDao = mock.MagicMock()
    mocked_user_controller = UserController(mockedDao)
    return mocked_user_controller

def test_getEmail_true(sut):
    email = 'jane.doe@gmail.com'
    sut.dao.find.return_value = [{'email': 'jane.doe@gmail.com'}]
    result = (UserController.get_user_by_email(sut, email)['email'] == email)
    assert result == True

def test_getEmail_false(sut):
    email = 'No.account@cassino.com'
    sut.dao.find.return_value = None
    result = (UserController.get_user_by_email(sut, email) == None)
    assert result == True

def test_getEmail_multi(sut):
    email = 'jane.doe@gmail.com'
    sut.dao.find.return_value = [{'email': 'jane.doe@gmail.com'}, {'email': 'jane.doe@gmail.com'}]
    result = (len(UserController.get_user_by_email(sut, email)) == 1)
    assert result

def test_getEmail_invalid(sut):
    email = 'Not an email'
    sut.dao.find.return_value = [{'email': 'jane.doe@gmail.com'}]
    with pytest.raises(ValueError) as errorInfo:
        UserController.get_user_by_email(sut, email)
    
    result = str(errorInfo.value) == 'Error: invalid email address'
    assert result

def test_getEmail_database_error(sut):
    email = 'jane.doe@gmail.com'
    sut.dao.find.side_effect = Exception('DataBase error')
    with pytest.raises(Exception) as errorInfo:
        UserController.get_user_by_email(sut, email)
    
    result = str(errorInfo.value) == 'DataBase error'
    assert result