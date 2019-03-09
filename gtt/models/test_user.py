import pytest
from gtt import db
from gtt.models import User
from gtt.fixtures import database


@pytest.mark.usefixtures("database")
def test_create_read():
    """Create a user in the database and read it back
    """
    write_user = User()
    write_user.username = "Hammer On"
    write_user.hashed_password = "3"
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
