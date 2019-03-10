"""Fixtures to use in unit tests"""
from pathlib import Path
import pytest
from flask import g
from gtt.models import Work, User
import gtt

@pytest.fixture(scope="session")
def database():
    """Create an in-memory database to use for testing, instantiated with the
    SQL from db/init.sql"""
    gtt.app.test_client()
    with gtt.app.app_context():
        g.db = gtt.db.create_sqlite3(":memory:")
        init_sql = Path("db/init.sql").read_text()
        g.db.executescript(init_sql)

        yield g.db

@pytest.fixture
def client():
    return gtt.app.test_client()

@pytest.fixture
def basic_work():
    """Create a work in the DB"""
    write_work = Work()
    write_work.name = "Song"
    write_work.save()
    yield write_work

    write_work.remove()

@pytest.fixture
def basic_user():
    """Create a user in the DB"""
    write_user = User()
    write_user.username = "Name"
    write_user.hashed_password = "H45H P455W0RD"
    write_user.save()
    yield write_user

    write_user.remove()
