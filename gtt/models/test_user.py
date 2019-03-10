import pytest
from gtt import db
from gtt.models import User, LoginFailedError
from gtt.fixtures import database, basic_user

# Required for fixtures
# pylint: disable=redefined-outer-name

@pytest.mark.usefixtures('database')
def test_create_read():
    """Create a user in the database and read it back."""
    write_user = User()
    write_user.username = 'Tim Apple'
    write_user.hashed_password = '3'
    write_user.can_manage_works = True
    write_user.can_manage_techniques = False
    write_user.can_su = False
    write_user.save()
    read_user = User.find(user_id=write_user.id)
    assert read_user.id == write_user.id
    assert read_user.username == write_user.username
    assert read_user.hashed_password == write_user.hashed_password
    assert read_user.can_manage_works == write_user.can_manage_works
    assert read_user.can_manage_techniques == write_user.can_manage_techniques
    assert read_user.can_su == write_user.can_su

@pytest.mark.userfixtures('database')
def test_attempt_login_correct_password(basic_user):
    """Test setting a password hash, then logging in with it."""
    password = 'Plain Text Password'
    basic_user.set_password(password)
    basic_user.save()
    read_user = User.attempt_login(basic_user.username, password)
    # If here, password succeeded and username found
    # At least check it's the right user
    assert read_user.id == basic_user.id

@pytest.mark.userfixtures('database')
def test_attempt_login_incorrect_password(basic_user):
    """Test setting a password hash, then logging in with a different password
    """
    password = 'Plain Text Password'
    basic_user.set_password(password)
    basic_user.save()
    with pytest.raises(LoginFailedError):
        User.attempt_login(basic_user.username, 'Wrong Password')

@pytest.mark.userfixtures('database')
def test_attempt_login_incorrect_username(basic_user):
    """Test logging in with a correct password but incorrect username"""
    password = 'Plain Text Password'
    basic_user.set_password(password)
    basic_user.save()
    with pytest.raises(LoginFailedError):
        User.attempt_login('Wrong_username', password)
