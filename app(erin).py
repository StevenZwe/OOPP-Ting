from flask import Flask, render_template, request, flash, redirect, url_for, session
from wtforms import Form, StringField, validators, DateField, SelectField, SubmitField
from Locker import Locker
import shelve
from Forms import *
import tkinter
from tkinter import messagebox


app = Flask(__name__)
app.secret_key = 'secretkey'

@app.route('/CheckAvail')
def checkAvail():
    form = LockerForm(request.form)
    cform = CheckAvailForm(request.form)

    dateav = cform.dateav.data
    locationav = cform.locationav.data

    availableLockersObject = {
        'sSIT': ['L01'],
        'mSIT': ['L02'],
        'bSIT': ['L03'],
        'sSBM': ['B01'],
        'mSBM': ['B02'],
        'bSBM': ['B03'],
        'sSCL': ['N01'],
        'mSCL': ['N02'],
        'bSCL': ['N03']
    }

    db_read = shelve.open("storage.db")

    try:
        lockerList = db_read["locker"]
    except:
        lockerList = {}

    if request.method == 'POST' and form.validate():
        for date in lockerList:
            for location in lockerList:
                if dateav == date:
                    if locationav == location:
                        checkalert()
                    else:
                        pass
                else:
                    pass

    return render_template("Locker_Public.html", form=form)


@app.route('/lockers', methods=['GET', 'POST'])
def func_locker():
    form = LockerForm(request.form)

    db_read = shelve.open("storage.db")

    try:
        lockerList = db_read["locker"]
    except:
        lockerList = {}

    if request.method == 'POST' and form.validate():
        adminno = form.adminno.data
        date = form.date.data
        location = form.location.data
        size = form.size.data
        lockers = Locker(adminno, date, location, size)
        id = len(lockerList) + 1
        lockers.set_id(id)
        lockerList[id] = lockers
        db_read["locker"] = lockerList
        db_read.close()
        flash('Locker form submitted successfully!', 'success')
        return redirect(url_for('func_locker'))
    return render_template('locker.html', form=form)


def checkalert():
    messagebox.showerror("Error", "This slot is already booked!")
    #print('''<script>
    #alert('Already Booked!');
    #</script>''')

class RequiredIf(object):

    def __init__(self, *args, **kwargs):
        self.conditions = kwargs
    def __call__(self, form, field):
        for name, data in self.conditions.items():
            if name not in form._fields:
                validators.Optional()(field)
                condition_field = form._fields.get(name)
            else:
                if condition_field.data == data:
                    validators.DataRequired().__call__(form, field)
                else:
                    validators.Optional().__call__(form, field)



@app.route('/payment')
def payment():
    return render_template('paypal.html', form=form)




@app.route('/')
def default():
    form = LockerForm(request.form)
    return render_template('locker.html', form=form)


#@app.route('/locker', methods=['GET', 'POST'])
#def new():
#    form = LockerForm(request.form)
#    cform = CheckForm(request.form)
#
#    db_read = shelve.open("storage.db")
#
#    try:
#        lockerList = db_read["locker"]
#    except:
#        lockerList = {}
#
#    dateav = cform.dateav.data
#
#    if request.method == 'POST' and form.validate():
#        for date in lockerList:
#            if dateav == date:
#                checkalert()
#            else:
#                    adminno = form.adminno.data
#                    date = form.date.data
#                    location = form.location.data
#                    size = form.size.data
#
#                    lockers = Locker(adminno, date, location, size)
#                    id = len(lockerList) + 1
#                    lockers.set_id(id)
#                    lockerList[id] = lockers
#                    db_read["locker"] = lockerList
#                    db_read.close()
#                    flash('Locker form submitted successfully!', 'success')
#                    return redirect(url_for('new'))
#    return render_template('locker.html', form=form)





#class LockerForm(Form):
#    adminno = StringField('Admin Number')
#    date = DateField('Date', format='%Y-%m-%d')
#    location = SelectField('Locker Location', choices=[("SIT", "School of Information Technology"),
#                                                       ("SBM", "School of Business Management"),
#                                                       ("SCL", "School of Chemical and Life Sciences")])
#    size = SelectField('Locker Size', choices=[("small", "Small"), ("medium", "Medium"), ("big", "Big")])
#
#class CheckForm(Form):
#    dateav = DateField('Date Availability', format='%Y-%m-%d')


@app.route('/lockeradmin')
def lockeradmin():
    db_read = shelve.open("storage.db", "r")
    lockers = db_read['locker']
    print(lockers)
    list = []
    for id in lockers:
        list.append(lockers.get(id))
    db_read.close()
    return render_template('lockerAdmin.html', lockers=list)
#PUT CHECK ON TOP
#


if __name__ == '__main__':
    app.run()
