from flask import Flask, render_template, request, flash, redirect, url_for, session
from wtforms import Form, StringField, TextAreaField, RadioField, SelectField, validators, PasswordField
from register import *
from test4 import Booking
import functools



app = Flask(__name__)
app.secret_key = 'secret123'

class RequiredIf(object):

    def __init__(self, *args, **kwargs):
        self.conditions = kwargs

    def __call__(self, form, field):
        for name, data in self.conditions.items():
            if name not in form._fields:
                validators.Optional()(field)
            else:
                condition_field = form._fields.get(name)
                if condition_field.data == data:
                    validators.DataRequired().__call__(form, field)
                else:
                    validators.Optional().__call__(form, field)


class Booking_teachers_form(Form):
    name = SelectField('Teacher', choices=[('', 'Select'),('Lee Chit Boon', 'Lee Chit Boon'),
                                           ('Zwe', 'Zwe')], default=' ')
    time = SelectField('Time slot:  ', [validators.DataRequired()],
                           choices=[('', 'Select'), ('9am', '9am'), ('10am', '10am'),
                                    ('11am', '11am'), ('12pm', '12pm'), ('1pm', '1pm')],
                           default='')
    date = SelectField('Date', choices=[(' ','Select'),('11/12/18','11/12/18'),
                                        ('12/12/18', '12/12/18')], default=' ')


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


@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/planner')
def planner():
    return render_template('Planner.html')

@app.route('/createbooking', methods=['GET', 'POST'])
def new():
    form = Booking_teachers_form(request.form)

    db_read = shelve.open("booking.db")

    try:
        bookinglist = db_read["bookings"]
    except:
        bookinglist = {}
    if request.method == 'POST':
        name = form.name.data
        date = form.date.data
        time = form.time.data
        book = Booking(name, date, time)

        db_read2 = shelve.open("booking.db", "r")
        booking = db_read2["bookings"]

        for checking in booking:
            book_storage = (booking.get(checking))
            book_storage_name = book_storage.get_name()
            book_storage_date = book_storage.get_date()
            book_storage_time = book_storage.get_time()
            if name == book_storage_name and date == book_storage_date and time == book_storage_time:
                flash('Time slot has been book, please try another time slot', 'danger')
                return redirect(url_for('new'))
            else:
                pass

        id = len(bookinglist) + 1

        book.set_pubid(id)

        bookinglist[id] = book

        db_read["bookings"] = bookinglist

        db_read.close()

        flash('Sucessfully booked!', 'success')

        return redirect(url_for('viewbookings'))

    return render_template('booking.html', form=form)


@app.route('/viewbookings')
def viewbookings():


    db_read = shelve.open("booking.db")
    try:
        booking = db_read["bookings"]
    except:
        booking = {}


    print(booking)

    list = []

    for pubid in booking:
        list.append(booking.get(pubid))

    return render_template('view_all_bookings.html', bookings=list)

@app.route('/Room_Booking')
def Room_Bookinng():
    return render_template('Room_Booking.html')



if __name__ == '__main__':
    app.run()

