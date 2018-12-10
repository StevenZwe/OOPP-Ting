from flask import Flask, render_template, request, flash, redirect, url_for, session
from wtforms import Form, StringField, TextAreaField, RadioField, SelectField, validators, PasswordField
import shelve
from register import *
import functools
# import firebase_admin
# from firebase_admin import credentials, db

# cred = credentials.Certificate('cred/library-system-a3843-firebase-adminsdk-av5pi-b432c9b613.json')
# default_app = firebase_admin.initialize_app(cred, {
#     'databaseURL': 'https://library-system-a3843.firebaseio.com/'
#
# })
#
# root = db.reference()
app = Flask(__name__)
app.secret_key = 'secret123'
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if session['id'] is None:
            return redirect(url_for('login'))
        return view(**kwargs)
    return wrapped_view

@app.route('/init')
def init():
    init_db()
    return 'db initialised'

@app.route('/home')
def home():
    return render_template('Login.html')


@app.route('/login',  methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        else:
            user = get_user(username, password)
            if user is None:
                error = 'Wrong username or password'
            else:
                session['id'] = user.get_id()
                session['user_name'] = user.get_username()
                return redirect(url_for('home'))
        flash(error, 'danger')
    return render_template('Login2.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))


class LoginForm(Form):
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    email=StringField('email',[validators.DataRequired()])
    name=StringField('name',[validators.DataRequired()])


@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        #email,password,username, full name,
        username = request.form['username']
        password = request.form['password']
        email=request.form['email']
        name=request.form['name']
        error = None
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not email:
            error = 'Email is required.'
        elif not name:
            error = 'Name is required.'
        else:
            create_user(username,password,email,name)
            return redirect(url_for('login'))
        flash(error)
    return render_template('register.html')

if __name__ == '__main__':

    app.run()
