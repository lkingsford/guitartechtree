import pytest
from gtt.models import WorkLink, LinkType
from gtt.fixtures import basic_work, database

# Required for fixtures
# pylint: disable=redefined-outer-name
# pylint: disable=unused-import

@pytest.mark.usefixtures("database")
def test_create_read(basic_work):
    """Create a WorkLink in the database and read it back
    """
    write_work_link = WorkLink()
    write_work_link.href = "http://example.com"
    write_work_link.link_type = LinkType.STREAM
    write_work_link.work_id = basic_work.id
    write_work_link.save()
    read_work_link: WorkLink = WorkLink.find(write_work_link.id)
    assert read_work_link.id == write_work_link.id
    assert read_work_link.href == write_work_link.href
    assert read_work_link.link_type == write_work_link.link_type
    assert read_work_link.work_id == write_work_link.work_id