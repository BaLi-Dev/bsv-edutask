import pytest
from unittest.mock import MagicMock
from src.util.dao import DAO
from src.controllers.usercontroller import UserController

@pytest.mark.unit
@pytest.fixture
def instance():
    """
    Fixture to create an instance of YourClass with a mocked DAO.
    """
    # Create the DAO mock based on the DAO specification.
    dao_mock = MagicMock(spec=DAO)
    # Pass the dao mock to the UserController constructor.
    obj = UserController(dao=dao_mock)
    return obj

@pytest.mark.unit
def test_invalid_email(instance):
    """
    Test that an invalid email raises a ValueError.
    """
    with pytest.raises(ValueError):
        instance.get_user_by_email('invalid-email')

@pytest.mark.unit
def test_no_user_found(instance):
    """
    Test that it returns None when no user is found for a given email.
    """
    wrong_email="user@example.com"
    instance.dao.find.return_value = []
    result = instance.get_user_by_email(wrong_email)
    assert result is None
    instance.dao.find.assert_called_once_with({'email': wrong_email})


@pytest.mark.unit
def test_one_user_found(instance):
    """
    Test that it returns None when no user is found for a given email.
    """
    right_email="user@example.com"
    expected_user = {"id": 1, "email": right_email}
    instance.dao.find.return_value = [expected_user]
    result = instance.get_user_by_email(right_email)
    assert result == expected_user
    instance.dao.find.assert_called_once_with({'email': right_email})

@pytest.fixture
def two_users():
    """
    Returns:
      email (str): the duplicate email
      user1 (dict): first user dict
      user2 (dict): second user dict
      users (list): [user1, user2]
    """
    email = "user@example.com"
    user1 = {"id": 1, "email": email}
    user2 = {"id": 2, "email": email}
    return email, user1, user2, [user1, user2]


@pytest.mark.unit
def test_logs_error_when_multiple_users_found(instance, two_users, capfd):
    email, user1, user2, users = two_users
    instance.dao.find.return_value = users

    # Act
    instance.get_user_by_email(email)

    # Assert: it printed the “more than one user” error
    out = capfd.readouterr().out
    assert f"Error: more than one user found with mail {email}" in out


@pytest.mark.unit
def test_returns_first_user_when_multiple_users_found(instance, two_users):
    email, user1, user2, users = two_users
    instance.dao.find.return_value = users

    # Act
    result = instance.get_user_by_email(email)

    # Assert: it returns the first user
    assert result == user1

@pytest.mark.unit
def test_dao_exception_propagates(instance):
    valid_email = "user@example.com"
    instance.dao.find.side_effect = Exception("Database error")

    with pytest.raises(Exception, match="Database error"):
        instance.get_user_by_email(valid_email)
