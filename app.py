from flask import *
from flask import Flask, render_template, request, flash, redirect, url_for
from wtforms import Form, StringField, TextAreaField, SelectField, validators
from Locker import *
import shelve

app = Flask(__name__)
app.secret_key = 'secret'

@app.route('/locker', methods=['GET', 'POST'])
def locker():
    form = RentalForm(request.form)
    if request.method == 'POST':
        adminno = form.adminno.data
        date = form.date.data
        location = form.location.data
        size = form.size.data
        error = None
        if not adminno:
            error = 'Admin Number is required.'
        elif not date:
            error = 'Date is required.'
        elif not location:
            error = 'Location of locker is required'
        elif not size:
            error = 'Size of locker is required'
        else:
            return redirect(url_for('login'))
        flash(error)
    return render_template('locker.html', form=form)

#@app.route('/')
#def default():
#    form = LockerForm(request.form)
#    return render_template('lockers.html', form=form)


#@app.route('/lockers', methods=['GET', 'POST'])
#def new():
#    form = LockerForm(request.form)
#
#    db_read = shelve.open("storage.db")
#
#    try:
#        lockersList = db_read["lockers"]
#    except:
#        lockersList = {}
#
#    if request.method == "POST" and form.validate():
#        adminno = form.adminno.data
#        date = form.date.data
#        location = form.location.data
#        size = form.size.data
#        lockers = Locker(adminno, date, location, size, submit)
#        id = len(lockersList) + 1
#        lockerid.set_id(id)
#        lockersList[id] = lockerid
#        db_read["lockers"] = lockersList
#        db_read.close()
#        flash("Locker form sent successfully!", 'success')
#        return redirect(url_for('new'))
#    return render_template('lockers.html', form=form)


#class RequiredIf(object):
#
#    def __init__(self, *args, **kwargs):
#        self.conditions = kwargs
#
#    def __call__(self, form, field):
#        for name, data in self.conditions.items():
#            if name not in form._fields:
#                validators.Optional()(field)
#            else:
#                condition_field = form._fields.get(name)
#                if condition_field.data == data:
#                    validators.DataRequired().__call__(form, field)
#                else:
#                    validators.Optional().__call__(form, field)
#
#class LockerForm(Form):
#    adminno = StringField('Admin No.', [validators.Length(min=7, max=7)])
#    date = DateField('Date', [validators.DataRequired("Please enter a date")])
#    location = SelectField('Locker Location', choice=[("blka", "Block A"), ("blkl", "Block L"), ("blks", "Block S"),
#                                                      ("blkk", "Block K"), ("blkb", "Block B")])
#    size = SelectField('Locker Size', choice=[("small", "Small"), ("medium", "Medium"), ("big", "Big")])
#    submit = SubmitField('Submit')
#
#class CheckForm(Form):
#    dateav = DateField('Date')
#    locationav = SelectField('Locker Location', choice=[("blka", "Block A"), ("blkl", "Block L"), ("blks", "Block S"),
#                                                        ("blkk", "Block K"), ("blkb", "Block B")])
#    submit = SubmitField('Check Availability')





if __name__ == '__main__':
    app.run(debug=True)
