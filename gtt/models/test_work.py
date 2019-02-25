import pytest
from gtt import db
from gtt.models import Work
from gtt.fixtures import database


@pytest.mark.usefixtures("database")
def test_create_read():
    """Create a work in the database and read it back
    """
    write_work = Work()
    write_work.name = "Song"
    write_work.save()
    read_work = Work.find(write_work.id)
    assert(read_work.id == write_work.id)
    assert(read_work.name == write_work.name)