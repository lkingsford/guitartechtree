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


@pytest.mark.usefixtures("database")
def test_attach_read_link(basic_work: Work):
    """Create a work in the database, create a link, attach the link
    to the work. Read back the link to see if it's there."""

    href = "http://example.com"
    link_type = LinkType.STREAM
    basic_work.add_link(href, link_type)

    read_links = basic_work.links()
    assert len(read_links) == 1
    assert read_links[0].href == href
    assert read_links[0].link_type == link_type
    assert read_links[0].work_id == basic_work.id

@pytest.mark.usefixtures("database")
def test_find_all():
    """Write 3 works to the database, then test that they are returned with
    find_all()"""
    for i in range(3):
        work = Work()
        work.name = str(i)
        work.save()
    works = Work.find_all()
    for i in range(3):
        assert works[i].name == str(i)
    assert len(works) == 3