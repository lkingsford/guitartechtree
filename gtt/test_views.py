"""Test the views in views.py"""

import gtt.views
from gtt.fixtures import client, basic_user, database

# Required for fixtures
# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument

def test_basic_login(basic_user, client, database):
    """Test that logging in with a correct username and password returns a
    an OK status"""
    password = 'Password'
    basic_user.set_password(password)
    basic_user.save()
    response = client.post('/login', data=dict(
        username=basic_user.username,
        password=password))
    assert response.status_code == 200

def test_login_fail(basic_user, client, database):
    """Test that logging in with an incorrect password results in a 401"""
    password = 'Password'
    basic_user.set_password(password)
    basic_user.save()
    response = client.post('/login', data = dict(
        username=basic_user.username,
        password='Incorrect Password'))
    assert response.status_code == 401