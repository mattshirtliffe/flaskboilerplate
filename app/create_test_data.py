

from db import db
from models import User
from models import Entries


def create_test_data():
    new_user = User('testuser','test@test.com','password')
    entry = Entries('words','more words',new_user)
    db.session.add(new_user)
    db.session.add(entry)
    db.session.commit()