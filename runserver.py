from app import app
from app.models import User
from app.models import Entries
from app.db import db



@app.cli.command('initdb')
def initdb_command():

    print('Initialized the database.')
    db.create_all()


@app.cli.command('create')
def create_entries():
    new_user = User('testuser','test@test.com','password')
    entry = Entries('words','more words',new_user)
    db.session.add(new_user)
    db.session.add(entry)
    db.session.commit()
    print 'done \n'



if __name__ == "__main__":
    app.run(debug=True)
