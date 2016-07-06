from app import app

from app import login_manager
from app.models import Entries
from app.models import User

from db import get_db, db

from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.exc import IntegrityError


@app.route('/index')
def index():
    error = None
    return render_template('base.html', error=error)

@app.route('/')
def show_entries():
    entries = Entries.query.order_by('id desc').all()
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
@login_required
def add_entry():
    if not session.get('logged_in'):
        abort(401)

    entry = Entries(request.form['title'], request.form['text'],current_user)
    db.session.add(entry)
    db.session.commit()

    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    remember = False
    if request.method == 'POST':
        if request.form['username']:
            username = request.form['username']
        if request.form['password']:
            password = request.form['password']
        try:
            if request.form['remember']:
                if request.form['remember'] == 'on':
                    remember = True
        except:
            remember = False
        user = User.query.filter_by(username=username).first()
        if user:
            password_ok = user.check_password(password)
            if password_ok:
                login_user(user,remember=remember)
                next = request.args.get('next')
                session['logged_in'] = True
                flash('You were logged in')
                return redirect(url_for('show_entries'))
            else:
                flash('incorrect username or password')
                return redirect(url_for('login'))
        else:
            flash('incorrect username or password')
            return redirect(url_for('login'))
    return render_template('login.html', error=error)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        if request.form['email']:
            email = request.form['email']
        else:
            error = 'email required'

        if request.form['username']:
            username = request.form['username']
        else:
            error = 'username required'


        if request.form['password']:
            password = request.form['password']
        else:
            error = 'password required'

        if error:
            return render_template('register.html', error=error)
        else:

            try:
                new_user = User(username, email, password)
                db.session.add(new_user)
                db.session.commit()
                flash('Successfully registered')
                return redirect(url_for('login'))
            except IntegrityError as e:
                flash('User with the email/username already exists')
                return redirect(url_for('register'))
            except Exception as e:
                flash('Error check exception')
                return redirect(url_for('register'))
    else:
        return render_template('register.html', error=error)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You were logged out')
    return redirect(url_for('show_entries'))