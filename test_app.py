# -*- coding: utf-8 -*-
"""
    App Tests
    ~~~~~~~~~~~~

    Tests the application.

"""

import pytest

from app import app
from app import config

from app.models import User, Entries
from app.db import db, init_db


def create_test_data():
    try:
        new_user = User('testuser','test@test.com','password')
        entry = Entries('words','more words',new_user)
        db.session.add(new_user)
        db.session.add(entry)
        db.session.commit()
    except:
        pass


@pytest.fixture
def client(request):


    client = app.test_client()
    app.config.from_object(config.TestingConfig)
    with app.app_context():
        init_db()

    def teardown():
        db.reflect()
        db.drop_all()

    return client


def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)


def test_empty_db(client):
    """Start with a blank database."""
    rv = client.get('/')
    assert b'No entries here so far' in rv.data


def test_login_logout(client):
    create_test_data()
    """Make sure login and logout works"""
    rv = login(client, app.config['USERNAME'],
               app.config['PASSWORD'])
    assert b'You were logged in' in rv.data
    rv = logout(client)
    assert b'You were logged out' in rv.data



def test_messages(client):
    """Test that messages work"""
    login(client, app.config['USERNAME'],
          app.config['PASSWORD'])
    rv = client.post('/add', data=dict(
        title='<Hello>',
        text='<strong>HTML</strong> allowed here'
    ), follow_redirects=True)
    assert b'No entries here so far' not in rv.data
    assert b'&lt;Hello&gt;' in rv.data
    assert b'<strong>HTML</strong> allowed here' in rv.data
