from flask import Flask, render_template, request, flash, redirect, url_for, session
from wtforms import Form, StringField, TextAreaField, RadioField, SelectField, validators, PasswordField
from test4 import Booking
import shelve

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



class PublicationForm(Form):
    name = SelectField('Teacher', choices=[('', 'Select'),('Lee Chit Boon', 'Lee Chit Boon'),
                                           ('Zwe', 'Zwe')], default=' ')
    time = SelectField('Time slot:  ', [validators.DataRequired()],
                           choices=[('', 'Select'), ('9am', '9am'), ('10am', '10am'),
                                    ('11am', '11am'), ('12pm', '12pm'), ('1pm', '1pm')],
                           default='')
    date = SelectField('Date', choices=[(' ','Select'),('11/12/18','11/12/18'),
                                        ('12/12/18', '12/12/18')], default=' ')


@app.route('/createbooking', methods=['GET', 'POST'])
def new():
    form = PublicationForm(request.form)
    db_read = shelve.open("booking.db")

    try:
        bookinglist = db_read["bookings"]
    except:
        bookinglist = {}

    if request.method == 'POST':
        name = form.name.data
        date = form.date.data
        time = form.time.data
        book=Booking(name,date,time)
        id = len(bookinglist) + 1

        book.set_pubid(id)

        bookinglist[id] = book

        db_read["bookings"] = bookinglist

        db_read.close()

        flash('Booking successfully requested.', 'success')

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