import pytest
from gtt import db
from gtt.models import Technique
from gtt.fixtures import database


@pytest.mark.usefixtures("database")
def test_create_read():
    """Create a technique in the database and read it back
    """
    write_technique = Technique()
    write_technique.name = "Hammer On"
    write_technique.short_description = "Rapidly pull on and off the string"
    write_technique.save()
    read_technique = Technique.find(write_technique.id)
    assert read_technique.id == write_technique.id
    assert read_technique.name == write_technique.name
    assert read_technique.short_description == write_technique.short_description

@pytest.mark.usefixtures("database")
def test_create_update_read():
    """Create and update a technique in the database and read it back
    """
    write_technique = Technique()
    write_technique.name = "Hammer On"
    write_technique.short_description = "Rapidly pull on and off the string"
    write_technique.save()
    write_technique.name = "Pull off"
    write_technique.save()
    read_technique = Technique.find(write_technique.id)
    assert read_technique.id == write_technique.id
    assert read_technique.name == write_technique.name
    assert read_technique.short_description == write_technique.short_description
