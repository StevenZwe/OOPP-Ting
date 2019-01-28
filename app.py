from flask import Flask, render_template, request, flash, redirect, url_for, session,make_response
from wtforms import Form, StringField, TextAreaField, RadioField, SelectField, validators, \
    PasswordField, DateField, DateTimeField,TimeField
from register import User
from test4 import Booking
from validate import Roombooking

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


class Booking_teachers_form(Form):
    name = SelectField('Teacher', choices=[('', 'Select'),('Lee Chit Boon', 'Lee Chit Boon'),
                                           ('Zwe', 'Zwe')], default=' ')
    time = SelectField('Time slot:  ', [validators.DataRequired()],
                           choices=[('', 'Select'), ('9am', '9am'), ('10am', '10am'),
                                    ('11am', '11am'), ('12pm', '12pm'), ('1pm', '1pm')],
                           default='')
    date = SelectField('Date', choices=[(' ','Select'),('11/12/18','11/12/18'),
                                        ('12/12/18', '12/12/18')], default=' ')

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


'''if request.cookies.get('admin_no') == admin_no:
show'''

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

@app.route('/timetable')
def timetable():
    return render_template('Timetable.html')



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


@app.route('/createbooking', methods=['GET', 'POST'])
def new():
    form = Booking_teachers_form(request.form)
    db_read = shelve.open("booking.db")

    try:
        bookinglist = db_read["bookings"]
    except:
        bookinglist = {}

    db_read = shelve.open("confirm.db")
    try:
        confirmlist = db_read["confirms"]
    except:
        confirmlist = {}

    if request.method == 'POST':
        name = form.name.data
        date = form.date.data
        time = form.time.data
        book=Booking(name,date,time)

        if bookinglist != {}:
            db_read2 = shelve.open("booking.db", "r")
            booking = db_read2["bookings"]

            for checking in booking:
                book_storage = (booking.get(checking))
                book_storage_name =  book_storage.get_name()
                book_storage_date = book_storage.get_date()
                book_storage_time = book_storage.get_time()
                if name == book_storage_name and date == book_storage_date and time == book_storage_time:
                    flash('Time slot has been book, please try another time slot', 'danger')
                    return redirect(url_for('new'))
                else:
                    pass

        if confirmlist != {}:
            db_readconfirm = shelve.open("confirm.db", "r")
            confirm = db_readconfirm["bookings"]

            for checking in confirm:
                confirm_storage = (confirm.get(checking))
                confirm_storage_name =  confirm_storage.get_name()
                confirm_storage_date = confirm_storage.get_date()
                confirm_storage_time = confirm_storage.get_time()
                if name == confirm_storage_name and date == confirm_storage_date and time == confirm_storage_time:
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


        flash('Room Booking Sucessfully.', 'success')

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



    try:
        rooms = db_read["rooms"]
    except:
        roomList = {}

    if request.method == 'POST':
        date = room_booking.date.data
        admin = Roombooking.admin.data
        room_no = room_booking.room_no.data
        if roomList == {}:
            roomList[date] = []
            roomList[date].append(admin)
            db_read["rooms"] = rooms
            db_read.close()
        else:
            if date in roomList:
                if room_no in roomList:
                    flash("Room already booked!", "warning")
                else:
                    roomList[date].append(admin)
                    db_read["rooms"] = roomList
                    db_read.close()
            else:
                roomList[date].append(admin)
                db_read["rooms"] = roomList
                db_read.close()

    return render_template('view_room.html', rooms=list)

@app.route('/viewconfirm')
def viewconfirm():


    db_read = shelve.open("confirm.db")
    try:
        confirm = db_read["confirms"]
    except:
        confirm = {}


    print(confirm)

    list = []

    for newid in confirm:
        list.append(confirm.get(newid))

    return render_template('view_confirm_bookings.html', confirms=list)


@app.route('/teacherbooking')
def teacherbooking():

    db_read = shelve.open("booking.db")
    try:
        booking = db_read["bookings"]
    except:
        booking = {}

    print(booking)

    list = []

    for pubid in booking:
        list.append(booking.get(pubid))

    db_read.close()

    return render_template('view_all_bookings_teacher.html', bookings=list)



@app.route('/reject_booking/<int:id>', methods=['POST'])
def reject_booking(id):
    db_read = shelve.open("booking.db")

    try:
        bList = db_read["bookings"]
        print("id, ", id)
        print("bList before: ", bList)

        ##del pList[id]
        bList.pop(id)

        print(bList)
        db_read["bookings"] = bList
        db_read.close()

        flash('Booking Rejected', 'success')

        return redirect(url_for('teacherbooking'))

    except:
        flash('Booking Not Rejected', 'danger')
        return redirect(url_for('teacherbooking'))


@app.route('/accept_booking/<int:id>', methods=['POST'])
def accept_booking(id):
    db_read = shelve.open("booking.db")
    db_newread=shelve.open('confirm.db')

    try:
        newList = db_newread['confirms']
    except:
        newList = {}

    try:

        bList = db_read["bookings"]
        print("id, ", id)
        book_storage = (bList.get(id))
        newid = len(newList) + 1

        book_storage.set_pubid(newid)

        newList[newid] = book_storage

        db_newread["confirms"] = newList

        db_newread.close()

        bList.pop(id)

        print(bList)
        db_read["bookings"] = bList
        db_read.close()

        flash('Booking Accepted', 'success')

        return redirect(url_for('teacherbooking'))

    except:
        flash('Booking Not Accepted', 'danger')
        return redirect(url_for('teacherbooking'))


@app.route('/testview')
def testview():
    return render_template('testview.html')



@app.route('/',  methods=('GET', 'POST'))
def login():
    db_read = shelve.open("user.db")
    try:
        userlist = db_read["users"]
    except:
        userlist = {}
    if request.method == 'POST':
        admin_no = request.form['admin_no']
        password = request.form['password']
        error = None

        if not admin_no:
            error = 'Admin Number is required.'
        elif not password:
            error = 'Password is required.'
        else:
            if userlist != {}: #to check if database is empty or not, if is empty return as flash
                db_read2 = shelve.open("user.db", "r")
                user = db_read2["users"]

                for checking in user:
                    user_storage = (user.get(checking))
                    user_storage_admin_no = user_storage.get_admin_no()
                    user_storage_password=user_storage.get_password()
                    user_storage_name = user_storage.get_name()
                    user_storage_identity = user_storage.get_identity()
                    user_storage_userid=user_storage.get_userid()
                    if user_storage_admin_no != admin_no or user_storage_password != password:
                        if user_storage_identity=='teacher' and user_storage_name==admin_no and user_storage_password==password:
                                session['id'] = admin_no
                                session['user_admin_No'] = admin_no
                                session['logged_in'] = True
                                session['identity']=user_storage_identity
                                resp = make_response(redirect(url_for('home')))
                                resp.set_cookie('admin_no',admin_no)  #key and value
                                return resp
                    else:
                        session['id'] = user_storage_userid
                        session['user_admin_No'] = user_storage_admin_no
                        session['identity']=user_storage_identity
                        session['logged_in'] = True
                        resp = make_response(redirect(url_for('home')))
                        resp.set_cookie('admin_no', admin_no)  # key and value
                        return resp
                        return redirect(url_for('home'))

            flash('Wrong admin number or password', 'danger')
    return render_template('Login2.html')

@app.route('/logout')
def logout():
    global check_for_id
    check_for_id= False
    session.pop('logged_in', None)
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = LoginForm(request.form)
    db_read = shelve.open("user.db")
    try:
        userlist = db_read["users"]
    except:
        userlist = {}
        # name,admin_no,password,email,school,course_name,pem_class
    if request.method == 'POST' and form.validate():
        admin_no = request.form['admin_no']
        password = request.form['password']
        email=request.form['email']
        name=request.form['name']
        school=request.form['school']
        course_name = request.form['course_name']
        pem_class = request.form['pem_class']
        error = None
        if not admin_no:
            error = 'Admin number is required.'
        elif not password:
            error = 'Password is required.'
        elif not email:
            error = 'Email is required.'
        elif not name:
            error = 'Name is required.'
        elif not pem_class:
            error = 'PEM class is required.'
        elif not school:
            error = 'School is required.'
        elif not course_name:
            error = 'Course name is required.'

        else:
            userz = User(admin_no,password,email,name,school,course_name,pem_class,'student')
            if userlist != {}:
                db_read2 = shelve.open("user.db", "r")
                user = db_read2["users"]

                for checking in user:
                    user_storage = (user.get(checking))
                    user_storage_admin_no = user_storage.get_admin_no()

                    if admin_no == user_storage_admin_no:
                        flash('You already have an  account', 'danger')
                        return redirect(url_for('register'))
                    else:
                        pass
            id = len(userlist) + 1

            userz.set_userid(id)

            userlist[id] = userz

            db_read["users"] = userlist

            db_read.close()
            return redirect(url_for('login'))
        flash(error)
    return render_template('Register.html',form=form)

@app.route('/register_teacher', methods=['GET', 'POST'])
def register_teacher():
    form = Login_teacherForm(request.form)
    db_read = shelve.open("user.db")
    try:
        userlist = db_read["users"]
    except:
        userlist = {}
        # name,admin_no,password,email,school,course_name,pem_class
    if request.method == 'POST' and form.validate():

        password = request.form['password']
        email=request.form['email']
        name=request.form['name']
        school=request.form['school']
        error = None
        if not password:
            error = 'Password is required.'
        elif not email:
            error = 'Email is required.'
        elif not name:

            error = 'Name is required.'

        elif not school:
            error = 'School is required.'

        else:
            userz = User('', password, email, name, school, '', '','teacher')
            if userlist != {}:
                db_read2 = shelve.open("user.db", "r")
                user = db_read2["users"]

                for checking in user:
                    user_storage = (user.get(checking))
                    user_storage_name = user_storage.get_name()

                    if name ==user_storage_name:
                        flash('You already have an  account', 'danger')
                        return redirect(url_for('register_teacher'))
                    else:
                        pass
            id = len(userlist) + 1

            userz.set_userid(id)

            userlist[id] = userz

            db_read["users"] = userlist

            db_read.close()
            return redirect(url_for('login'))
        flash(error)
    return render_template('Register_teacher.html',form=form)
  #WTForms for Register
class LoginForm(Form):
    admin_no = StringField('Admin Number', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    email=StringField('Email',[validators.DataRequired()])
    name=StringField('Name',[validators.DataRequired()])
    pem_class = StringField('PEM Class', [validators.DataRequired()])
    school = SelectField('School',[validators.DataRequired()],
                         choices=[('', 'Select'),('SIT', 'SIT'),('SCL', 'SCL'),('SBM', 'SBM'),
                                 ('SIDM', 'SIDM'),('SEG', 'SEG'),('SHSS', 'SHSS'), ('SDM', 'SDM')
                                ], default=' ' )
    course_name=SelectField('Course',[validators.DataRequired()],
                         choices=[('', 'Select'),('DSF', 'Cyber Security and Forensics'),
                                  ('DIT', 'Information Technology'), ('BI', 'Business Informatics'),
                                  ('FI', 'Financial Informatics')], default=' ' )

class Login_teacherForm(Form):
    password = PasswordField('Password', [validators.DataRequired()])
    email=StringField('Email',[validators.DataRequired()])
    name=StringField('Name',[validators.DataRequired()])
    school = SelectField('School',[validators.DataRequired()],
                         choices=[('', 'Select'),('SIT', 'SIT'),('SCL', 'SCL'),('SBM', 'SBM'),
                                 ('SIDM', 'SIDM'),('SEG', 'SEG'),('SHSS', 'SHSS'), ('SDM', 'SDM')
                                ], default=' ' )


if __name__ == '__main__':
    app.run()


