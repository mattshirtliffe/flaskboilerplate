# -*- coding: utf-8 -*-

import os
from sqlite3 import dbapi2 as sqlite3

from app import app
from flask import g
from flask_sqlalchemy import SQLAlchemy


# from app import login_manager


# # Load default config and override config from an environment variable
# app.config.update(dict(
#     DATABASE=os.path.join(app.root_path, 'app.db'),
#     DEBUG=True,
#     SECRET_KEY='development key',
#     USERNAME='admin',
#     PASSWORD='default',
#     SQLALCHEMY_TRACK_MODIFICATIONS=True
# ))
#
# app.config.from_envvar('FLASKR_SETTINGS', silent=True)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'


db = SQLAlchemy(app)

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    """Initializes the database."""
    db.create_all()


@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    db.create_all()


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


