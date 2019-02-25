"""Fixtures to use in unit tests"""
from flask import g
from pathlib import Path
import pytest
import gtt
import sqlite3

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
