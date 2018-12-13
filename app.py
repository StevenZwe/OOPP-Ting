from flask import Flask, render_template, request, flash, redirect, url_for, session
from wtforms import Form, StringField, validators, DateField, SelectField
from Locker import Locker
import shelve


app = Flask(__name__)
app.secret_key = 'secretkey'


@app.route('/')
def default():
    form = LockerForm(request.form)
    return render_template('locker.html', form=form)


@app.route('/locker', methods=['GET', 'POST'])
def new():
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
        return redirect(url_for('new'))
    return render_template('locker.html', form=form)


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


class LockerForm(Form):
    adminno = StringField('Admin Number', [validators.length(min=7, max=7)])
    date = DateField('Date', format='%Y-%m-%d')
    location = SelectField('Locker Location', choices=[("blka", "Block A"), ("blkl", "Block L"), ("blks", "Block S")])
    size = SelectField('Locker Size', choices=[("small", "Small"), ("medium", "Medium"), ("big", "Big")])

#class CheckForm(Form):
#    dateav = DateField('Date', format='%Y-%m-%d')
#    locationav = SelectField('Locker Location', choices=[("blka", "Block A"), ("blkl", "Block L"), ("blks", "Block S")])


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


@app.route('/delete_lockeradmin/<int:id>', methods=['POST'])
def delete_locker(id):
    db_read = shelve.open("storage.db")

    try:
        list = db_read["locker"]
        print("id,",id)
        print("list before:", list)

        list.pop(id)

        print(list)
        db_read["locker"] = list
        db_read.close()

        flash('Locker Booking Deleted!', 'success')

        return redirect(url_for('lockeradmin'))

    except:
        flash('Slot not deleted!', 'danger')
        return redirect(url_for('lockeradmin'))


if __name__ == '__main__':
    app.run()

#roger taylor