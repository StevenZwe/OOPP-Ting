from flask import Flask, render_template, request, flash, redirect, url_for, session
from wtforms import Form, StringField, TextAreaField, RadioField, SelectField, validators, PasswordField, DateField, DateTimeField
from register import User
from test4 import Booking
from validate import Roombooking
from Planner import Planner
from Locker import Locker
import functools
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




class editPlanner(Form):
    task = StringField('Name of Task', [validators.DataRequired()])
    time = SelectField("Time", [validators.DataRequired()],
                       choices=[('', 'Select'), ('9am-10am', '9am-10am'), ('10am-11am', '10am-11am'),
                                ('11am-12pm', '11am-12pm'), ('12pm-1pm', '12pm-1pm'), ('1pm-2pm', '1pm-2pm'),
                                ('2pm-3pm', '2pm-3pm'), ('3pm-4pm', '3pm-4pm'), ('4pm-5pm', '4pm-5pm')], default=' ')
    date = SelectField("Date", choices=[(' ', 'Select'), ('11/12/18', '11/12/18'),
                                        ('12/12/18', '12/12/18')], default=' ')

    desc = StringField("Description")
    priority = SelectField("Importance", choices=[(' ', 'Select'), ('1 Star', '1 Star'),
                                        ('2 Star', '2 Star'),('3 Star', '3 Star'),
                                        ('4 Star', '4 Star'),('5 Star', '5 Star')], default='1 Star')


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if session['id'] is None:
            return redirect(url_for('login'))
        return view(**kwargs)
    return wrapped_view


@app.route('/get-cookie/')
def get_cookie():
    id = request.cookies.get('admin_no')
    name=request.cookies.get('name')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/avaliable_room')
def avaliable_room():
    return render_template('view_avaliable_room.html')




@app.route('/planner')
def planner():
    return render_template('Planner.html')


@app.route('/planneredit', methods=['GET','POST'])
def Editplanner():
    form = editPlanner(request.form)

    db_read = shelve.open("plans.db")
    try:
        planList = db_read["plan"]
    except:
        planList = {}

    if request.method == 'POST':
        task = form.task.data
        time = form.time.data
        date = form.date.data
        desc = form.desc.data
        priority = form.priority.data
        plan = Planner(task, date, time, desc ,priority)

        id = len(planList) + 1

        plan.set_pubid(id)

        planList[id] = plan

        db_read["plan"] = planList

        db_read.close()

        flash('Sucess!', 'success')

        return redirect(url_for('viewplans'))

    return render_template('planneredit.html', form=form)


@app.route('/viewplans')
def viewplans():


    db_read = shelve.open("plans.db")
    try:
        plan = db_read["plan"]
    except:
        plan = {}


    print(plan)

    list = []

    for id in plan:
        list.append(plan.get(id))

    return render_template('viewPlans.html', plan=list)


@app.route('/Room_Booking',  methods=('GET', 'POST'))
def roombooking():
    form = room_booking(request.form)
    db_read = shelve.open("room.db")

    try:
        roomlist = db_read["rooms"]
    except:
        roomlist = {}

    if request.method == 'POST':
        block = form.block.data
        date = form.date.data
        time = form.time.data
        room_no = form.room_no.data
        room = Roombooking(block, room_no, date, time,request.cookies.get('admin_no'))
        id = len(roomlist) + 1

        room.set_room_id(id)

        roomlist[id] = room

        db_read["rooms"] = roomlist

        db_read.close()

        flash('Magazine Inserted Sucessfully.', 'success')

        return redirect(url_for('viewroom'))

    return render_template('Room_Booking.html', form=form)


class room_booking(Form):
    time = SelectField('Time slot:  ', [validators.DataRequired()],
                           choices=[('', 'Select'), ('9am', '9am'), ('10am', '10am'),
                                    ('11am', '11am'), ('12pm', '12pm'), ('1pm', '1pm')],)
    block = SelectField('Block', choices=[('', 'Select'),('SBM', 'Blk B'),("SIDM","Blk M"),
                                           ('SIT', 'Blk L')], default=' ')
    room_no = SelectField('Room:  ', [validators.DataRequired()],
                           choices=[('', 'Select'),('Level 6', '601'), ('Level 6', '602'),('Level 6', '603'),('Level 6', '604'),('Level 6', '605'),
                                    ('Level 6', '606'),
                                    ('Level 6', '607'),
                                    ('Level 6', '608'),
                                    ('Level 6', '609'),
                                    ('Level 6', '610'),
                                    ('Level 5', '532'),
                                    ('Level 5', '503'), ('Level 4', '432'), ('Level 4', '407')],
                           default='')
    date = SelectField('Date', choices=[(' ','Select'),('11/12/18','11/12/18'),
                                        ('12/12/18', '12/12/18')], default=' ')


@app.route('/viewroom')
def viewroom():


    db_read = shelve.open("room.db")
    try:
        room = db_read["rooms"]
    except:
        room = {}


    print(room)

    list = []

    for room_id in room:
        list.append(room.get(room_id))

    return render_template('view_room.html', rooms=list)


if __name__ == '__main__':
    app.run()


