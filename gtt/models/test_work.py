import pytest
from gtt import db
from gtt.models import Work
from gtt.models import Technique
from gtt.models import LinkType
from gtt.fixtures import database, basic_work

# Required for fixtures
# pylint: disable=redefined-outer-name

@pytest.mark.usefixtures("database")
def test_create_read():
    """Create a work in the database and read it back
    """
    write_work = Work()
    write_work.name = "Song"
    write_work.save()
    read_work = Work.find(write_work.id)
    assert read_work.id == write_work.id
    assert read_work.name == write_work.name

@pytest.mark.usefixtures("database")
def test_attach_read_technique(basic_work: Work):
    """Create a work in the database, create a technique, attach the technique
    to the work. Read back the technique to see if it's there."""

    write_technique = Technique()
    write_technique.name = "Technique 1"
    write_technique.short_description = "Technique Description"
    write_technique.save()
    basic_work.add_technique(write_technique)

    read_techniques = basic_work.techniques()
    assert len(read_techniques) == 1
    assert read_techniques[0].name == write_technique.name


