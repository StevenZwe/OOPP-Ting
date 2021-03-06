from flask import Flask, render_template, request, flash, redirect, \
    url_for, send_from_directory, make_response, session
from wtforms import Form, StringField, TextAreaField,\
    RadioField, SelectField, validators, PasswordField,DateField,DateTimeField,TimeField
from register import User,Admin
from Bookingteachers import Booking
from Teacher_timetable import Teacher_timetable
import functools
import shelve
import json
import datetime
from validate import Roombooking
from Locker import Locker
from Forms import *
from Planner import *
from tkinter import *
from tkinter import messagebox
import os
from os.path import join, dirname, realpath
from werkzeug.utils import secure_filename



app = Flask(__name__)
app.secret_key = 'secret123'

UPLOAD_FOLDER1 = '/static/Documents/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER1
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOADS_PATH'] = join(dirname(realpath(__file__)), 'static\\Documents\\')

@app.route('/teacher_timetable/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOADS_PATH'], filename)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

class checklist(Form):
    Task = StringField('Name of Task', [validators.DataRequired()])
    Duration = SelectField("Duration", [validators.DataRequired()],
                       choices=[('', 'Select'), ('5 mins', '5 mins'), ('10 mins', '10 mins'),
                                ('15 mins', '15 mins'), ('30 mins', '30 mins'), ('45 mins', '45 mins'),
                                ('1 hour', '1 hour'), ('2 hours', '2 hours'), ('3 hours', '3 hours'),
                                ('4 hours', '4 hours'), ('Others', 'Others')], default='')

    Desc = StringField("Description")
    Priority = SelectField("Importance", choices=[(' ', 'Select (1 Star being least important, 5 being most)'),
                                    ('1 Star', '1 Star'),('2 Star', '2 Star'), ('3 Star', '3 Star'),
                                    ('4 Star', '4 Star'), ('5 Star', '5 Star')], default='')

class quickAdd(Form):
    Task = SelectField("Task", [validators.DataRequired()],
                       choices=[('', 'Select'), ('Exercise', 'Exercise'), ('Go Out', 'Go Out'),
                                ('Homework', 'Homework'), ('Revision', 'Revision'), ('Meeting', 'Meeting'),
                                ('Groceries', 'Groceries'), ('Chores', 'Chores'), ('Work', 'Work'),
                                ('Project', 'Project')], default='')
    Duration = SelectField("Duration",
                           choices=[('', 'Select'), ('5 mins', '5 mins'), ('10 mins', '10 mins'),
                                    ('15 mins', '15 mins'), ('30 mins', '30 mins'), ('45 mins', '45 mins'),
                                    ('1 hour', '1 hour'), ('2 hours', '2 hours'), ('3 hours', '3 hours'),
                                    ('4 hours', '4 hours'), ('Others', 'Others')], default='')
    Priority = SelectField("Importance", choices=[(' ', 'Select (1 Star being least important, 5 being most)'),
                                    ('1 Star', '1 Star'),('2 Star', '2 Star'), ('3 Star', '3 Star'),
                                    ('4 Star', '4 Star'), ('5 Star', '5 Star')], default='')


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
    db_read = shelve.open("booking.db")

    try:
        booking = db_read["bookings"]
    except:
        booking = {}

    print(booking)
    print('Hello')
    list3 = []

    for pubid in booking:
        list3.append(booking.get(pubid))
    print(list3)
    return render_template('home.html', booking=list3)


@app.route('/avaliable_room')
def avaliable_room():
    return render_template('view_avaliable_room.html')

@app.route('/timetable')
def timetable():
    return render_template('Timetable.html')

@app.route('/calendar')
def calendar():
    return render_template('calender.html')

@app.route('/quickList', methods=['GET','POST'])
def addQuick():
    form = quickAdd(request.form)

    db_read = shelve.open("plan.db")
    try:
        planList = db_read["plans"]
    except:
        planList = {}

    if request.method == 'POST':
        task = form.Task.data
        time = form.Duration.data
        date = request.form["Date"]
        priority = form.Priority.data
        plan = Planner(task, date, time, priority)
        id = len(planList) + 1
        plan.set_id(id)

        cal = Calendar()
        cal.set_id(id)
        cal.set_title(task)
        cal.set_start(date)
        cal.set_allDay()
        if priority == '1 Star':
            cal.set_color('#708090')
        if priority == '2 Star':
            cal.set_color('#bdc9e1')
        if priority == '3 Star':
            cal.set_color('#74a9cf')
        if priority == '4 Star':
            cal.set_color('#2c7fb8')
        if priority == '5 Star':
            cal.set_color('#253494')

        calTask = cal.__dict__
        dataList1 = []

        with open("events.json", "r") as input_data:
            data = json.load(input_data)
            for line in data:
                dataList1.append(line)

        with open("events.json", "w") as write_data:
            dataList1.append(calTask)
            json.dump(dataList1, write_data, indent=4)
            write_data.close()

        planList[id] = plan

        db_read["plans"] = planList

        db_read.close()

        flash('Success!', 'success')

        return redirect(url_for('calendar'))

    return render_template('quickList.html', form=form)

@app.route('/checklist', methods=['GET','POST'])
def addChecklist():
    form = checklist(request.form)

    db_read = shelve.open("plan.db")
    try:
        planList = db_read["plans"]
    except:
        planList = {}

    if request.method == 'POST':
        task = form.Task.data
        time = form.Duration.data
        date = request.form["Date"]
        desc = form.Desc.data
        color = request.form["color"]
        priority = form.Priority.data
        plan = Planner(task, date, time, priority)

        id = len(planList) + 1
        plan.set_desc(desc)
        plan.set_id(id)

        cal = Calendar()
        cal.set_id(id)
        cal.set_title(task)
        cal.set_start(date)
        cal.set_color(color)
        cal.set_allDay()

        planList[id] = plan
        calTask = cal.__dict__
        db_read["plans"] = planList

        db_read.close()
        dataList = []

        if not dataList:
            with open("events.json", "r") as input_data:
                data = json.load(input_data)
                for line in data:
                    dataList.append(line)

        with open("events.json", "w") as write_data:
            dataList.append(calTask)
            json.dump(dataList, write_data, indent=4)
            write_data.close()

        flash('Success!', 'success')

        return redirect(url_for('calendar'))

    return render_template('checklist.html', form=form, editing=False)

@app.route('/viewChecklist')
def viewChecklist():

    db_read = shelve.open("plan.db")
    try:
        plans = db_read["plans"]
    except:
        plans = {}

    list = []

    for id in plans:
        plan = plans.get(id)
        dateTime = plan.get_date()
        date = dateTime.split('T')
        newDate = date[0]
        plan.set_date(newDate)
        list.append(plan)
    return render_template('viewChecklist.html', plans=list)

@app.route('/edit_task/<int:id>', methods=['GET', 'POST'])
def update_task(id):
    form = checklist(request.form)
    db_read = shelve.open("plan.db")
    planList = db_read["plans"]
    plan1 = planList.get(id)
    try:
        if request.method == 'POST':
            task = form.Task.data
            date = request.form["Date"]
            time = form.Duration.data
            desc = form.Desc.data
            color = request.form["color"]
            priority = form.Priority.data
            plan = Planner(task, date, time, priority)
            plan.set_desc(desc)
            plan.set_id(id)

            planList[id] = plan
            db_read["plans"] = planList
            db_read.close()

            cal = Calendar()
            cal.set_id(id)
            cal.set_title(task)
            cal.set_start(date)
            cal.set_color(color)
            cal.set_allDay()

            dataList = []

            with open("events.json", "r") as input_data:
                data = json.load(input_data)
                for line in data:
                    dataList.append(line)

            with open("events.json", "w") as write_data:
                for event in dataList:
                    if event['id'] == id:
                        event["title"] = task
                        event["start"] = date
                        event["color"] = color
                        json.dump(dataList, write_data, indent=4)
                        write_data.close()
                flash('Success!', 'success')
                return redirect(url_for('calendar'))
    except :
            flash('HELP', 'danger')
            return  redirect(url_for('calendar'))

    return render_template('checklist.html', form=form, editing=True, plan1=plan1)


@app.route('/delete_task/<int:id>', methods=['POST'])
def delete_task(id):
    db_read = shelve.open("plan.db")

    try:
        dataList = []
        with open("events.json", "r") as input_data:
            data = json.load(input_data)
            for line in data:
                dataList.append(line)

        with open("events.json", "w") as edit_data:
            dataList.pop(id-1)
            json.dump(dataList, edit_data, indent=4)
            edit_data.close()

        planList = db_read["plans"]
        print("id, ", id)
        print("planList before: ", planList)

        ##del pList[id]
        planList.pop(id)
        print(planList)
        db_read["plans"] = planList
        db_read.close()
        flash('Done!', 'success')

        return redirect(url_for('viewChecklist'))

    except:
        flash('Not Done :(', 'danger')
        return redirect(url_for('viewChecklist'))

@app.route('/data')
def return_data():
    with open("events.json", "r") as input_data:
        return input_data.read()

@app.route('/Room_Booking',  methods=('GET', 'POST'))
def roombooking():
    form = room_booking(request.form)
    db_read = shelve.open("room.db")
    print('hi')
    try:
        roomlist = db_read["rooms"]
    except:
        roomlist = {}
    print('bye')

    if request.method == 'POST':
        block = form.block.data
        date = form.date.data
        time = form.time.data
        room_no = form.room_no.data
        print('zzz')

        room = Roombooking(block, room_no, date, time,request.cookies.get('admin_no'))
        try:
            rooms = db_read["rooms"]
        except:
            rooms = {}
        print('xzxzo')

        if request.method == 'POST':
            print('hi')
            if rooms != {}:
                for checking in rooms:
                    room_storage = (rooms.get(checking))
                    room_storage_block = room_storage.get_block()
                    room_storage_date = room_storage.get_date()
                    room_storage_room_no =room_storage.get_room_no()
                    room_storage_time= room_storage.get_time()
                    print('knn')

                    if block == room_storage_block and room_no == room_storage_room_no and date == room_storage_date and time == room_storage_time:
                        flash("Room has been booked, please book another room", "danger")
                        return redirect(url_for('roombooking'))
                print('xadasdas')

            id = len(roomlist) + 1

            room.set_room_id(id)

            roomlist[id] = room

            db_read["rooms"] = roomlist

            db_read.close()
            print('hi')
            flash('Room Booking Sucessfully', 'success')
            return redirect(url_for('viewroom'))

    return render_template('Room_Booking.html', form=form)

class room_booking(Form):
    time = SelectField('Time slot:  ', [validators.DataRequired()],
                           choices=[('', 'Select'), ('9am', '9am'), ('10am', '10am'),
                                    ('11am', '11am'), ('12pm', '12pm'), ('1pm', '1pm')],)
    block = SelectField('Block', choices=[('', 'Select'),('SBM', 'Blk B'),("SIDM","Blk M"),
                                           ('SIT', 'Blk L')], default=' ')
    room_no = SelectField('Room:  ', [validators.DataRequired()],
                           choices=[('', 'Select'),('Room 601', 'Room 601'), ('Room 602', 'Room 602'),('Room 603', 'Room 603'),('Room 604', 'Room 604'),('Room 605', 'Room 605'),
                                    ('Room 606', 'Room 606'),
                                    ('Room 607', 'Room 607'),
                                    ('Room 608', 'Room 608'),
                                    ('Room 609', 'Room 609'),
                                    ('Room 610', 'Room 610'),
                                    ('Room 532', 'Room 532'),
                                    ('Room 503', 'Room 503'), ('Room 432', 'Room 432'), ('Room 407', 'Room 407')],
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
    return render_template('view_room.html',rooms=list)

@app.route('/checkAvailability', methods=['GET', 'POST'])
def checkAvail():
    form = LockerForm(request.form)
    cform = CheckAvailForm(request.form)
    db_readcheck = shelve.open("check.db")
    lockertuple = ("L01", "L02", "L03", "L04", "N01", "N02", "N03", "N04", "B01", "B02", "B03", "B04")

    try:
        checkList = db_readcheck["checklist"]
    except:
        checkList = {}

    finallist = []

    if request.method == 'POST' and cform.validate():
        dateav = cform.dateav.data
        if dateav in checkList:
            #convert tuple to list
            lockerlist = list(lockertuple)
            #list of dates from database
            checkListList = checkList[dateav]
            finallist = [x for x in lockerlist if x not in checkListList]
            session['finallist'] = finallist
            print(finallist)
            db_readcheck.close()
        else:
            finallist = lockertuple
            session['finallist'] = finallist
            print(finallist)
            db_readcheck.close()

    return render_template("locker.html", cform=cform, form=form, finallist=finallist)

@app.route('/lockers', methods=['GET', 'POST'])
def func_locker():
    form = LockerForm(request.form)
    cform = CheckAvailForm(request.form)
    db_read = shelve.open("storage.db")
    db_readcheck = shelve.open("check.db")

    try:
        lockerList = db_read["locker"]
    except:
        lockerList = {}

    try:
        checkList = db_readcheck["checklist"]
    except:
        checkList = {}

    finallist = []

    print(checkList)
    print(lockerList)


    if request.method == 'POST' or form.validate():
        date = form.date.data
        lockerno = request.form['lockernohtml']
        #if checklist is empty (no one booked anything)
        if checkList == {}:
            flash('Locker form submitted successfully!', 'success')
            adminno = form.adminno.data
            date = form.date.data
            location = request.form['locationhtml']
            size = request.form['sizehtml']
            lockerno = request.form['lockernohtml']
            lockers = Locker(adminno, date, location, size, lockerno)
            id = len(lockerList) + 1
            lockers.set_id(id)
            lockerList[id] = lockers
            #
            session['adminno'] = adminno
            session['date'] = date
            session['lockerno'] = lockerno
            #
            if lockerno == 'L03' or lockerno == 'N03' or lockerno == 'B03':
                db_read["locker"] = lockerList
                db_read.close()
                #
                checkList[date] = []
                checkList[date].append(lockerno)
                db_readcheck["checklist"] = checkList
                db_readcheck.close()
                #
                session['adminno'] = adminno
                session['date'] = date
                session['lockerno'] = lockerno
                return redirect(url_for('paymentmedium'))
            elif lockerno == 'L04' or lockerno == 'N04' or lockerno == 'B04':
                db_read["locker"] = lockerList
                db_read.close()
                #
                checkList[date] = []
                checkList[date].append(lockerno)
                db_readcheck["checklist"] = checkList
                db_readcheck.close()
                #
                session['adminno'] = adminno
                session['date'] = date
                session['lockerno'] = lockerno
                return redirect(url_for('paymentbig'))
            else:
                db_read["locker"] = lockerList
                db_read.close()
                #
                checkList[date] = []
                checkList[date].append(lockerno)
                db_readcheck["checklist"] = checkList
                db_readcheck.close()
                #
                session['adminno'] = adminno
                session['date'] = date
                session['lockerno'] = lockerno
                return redirect(url_for('paymentsmall'))
        else:
            #if this date has been booked
            if date in checkList:
                ##for every lockerno in the list
                #if locker number is in list in that date then confirm booked
                if lockerno in checkList[date]:
                        flash('Locker %s is already booked! Please enter another locker number.' % (lockerno),
                              'warning')
                        return redirect(url_for('func_locker'))
                #if locker no is not in date then not booked but has list already
                else:
                    flash('Locker form submitted successfully!', 'success')
                    adminno = form.adminno.data
                    date = form.date.data
                    location = request.form['locationhtml']
                    size = request.form['sizehtml']
                    lockerno = request.form['lockernohtml']
                    lockers = Locker(adminno, date, location, size, lockerno)
                    id = len(lockerList) + 1
                    lockers.set_id(id)
                    lockerList[id] = lockers
                    #
                    if lockerno == 'L03' or lockerno == 'N03' or lockerno == 'B03':
                        db_read["locker"] = lockerList
                        db_read.close()
                        #
                        checkList[date].append(lockerno)
                        db_readcheck["checklist"] = checkList
                        db_readcheck.close()
                        #
                        session['adminno'] = adminno
                        session['date'] = date
                        session['lockerno'] = lockerno
                        return redirect(url_for('paymentmedium'))
                    elif lockerno == 'L04' or lockerno == 'N04' or lockerno == 'B04':
                        db_read["locker"] = lockerList
                        db_read.close()
                        #
                        checkList[date].append(lockerno)
                        db_readcheck["checklist"] = checkList
                        db_readcheck.close()
                        #
                        session['adminno'] = adminno
                        session['date'] = date
                        session['lockerno'] = lockerno
                        return redirect(url_for('paymentbig'))
                    else:
                        db_read["locker"] = lockerList
                        db_read.close()
                        #
                        checkList[date].append(lockerno)
                        db_readcheck["checklist"] = checkList
                        db_readcheck.close()
                        #
                        session['adminno'] = adminno
                        session['date'] = date
                        session['lockerno'] = lockerno
                        return redirect(url_for('paymentsmall'))
                print(2)
            # return redirect(url_for('func_locker'))

            else:
                flash('Locker form submitted successfully!', 'success')
                adminno = form.adminno.data
                date = form.date.data
                location = request.form['locationhtml']
                size = request.form['sizehtml']
                lockerno = request.form['lockernohtml']
                lockers = Locker(adminno, date, location, size, lockerno)
                id = len(lockerList) + 1
                lockers.set_id(id)
                lockerList[id] = lockers
                #
                if lockerno == 'L03' or lockerno =='N03' or lockerno == 'B03':
                    db_read["locker"] = lockerList
                    db_read.close()
                    #
                    checkList[date] = []
                    checkList[date].append(lockerno)
                    db_readcheck["checklist"] = checkList
                    db_readcheck.close()
                    #
                    session['adminno'] = adminno
                    session['date'] = date
                    session['lockerno'] = lockerno
                    return redirect(url_for('paymentmedium'))
                elif lockerno == 'L04' or lockerno == 'N04' or lockerno == 'B04':
                    db_read["locker"] = lockerList
                    db_read.close()
                    #
                    checkList[date] = []
                    checkList[date].append(lockerno)
                    db_readcheck["checklist"] = checkList
                    db_readcheck.close()
                    #
                    session['adminno'] = adminno
                    session['date'] = date
                    session['lockerno'] = lockerno
                    return redirect(url_for('paymentbig'))
                else:
                    db_read["locker"] = lockerList
                    db_read.close()
                    #
                    checkList[date] = []
                    checkList[date].append(lockerno)
                    db_readcheck["checklist"] = checkList
                    db_readcheck.close()
                    #
                    session['adminno'] = adminno
                    session['date'] = date
                    session['lockerno'] = lockerno
                    return redirect(url_for('paymentsmall'))

                # return redirect(url_for('func_locker'))
                print(3)

    return render_template('locker.html', form=form, finallist=finallist, cform=cform)

def lockerRedirect(lockerno):
    flash('Locker %s is already booked! Please enter another locker number.' % (lockerno),
          'warning')
    return redirect(url_for('func_locker'))


@app.route('/locker/payment/small')
def paymentsmall():
    adminno = session.get('adminno', None)
    date = session.get('date', None)
    lockerno = session.get('lockerno', None)
    flash('Please go to i@Central to collect your locker combination.', 'success')
    return render_template('paypalsmall.html', adminno=adminno, date=date, lockerno=lockerno)

@app.route('/locker/payment/medium')
def paymentmedium():
    adminno = session.get('adminno', None)
    date = session.get('date', None)
    lockerno = session.get('lockerno', None)
    flash('Please go to i@Central to collect your locker combination.', 'success')
    return render_template('paypalmedium.html', adminno=adminno, date=date, lockerno=lockerno)

@app.route('/locker/payment/big')
def paymentbig():
    adminno = session.get('adminno', None)
    date = session.get('date', None)
    lockerno = session.get('lockerno', None)
    flash('Please go to i@Central to collect your locker combination.', 'success')
    return render_template('paypalbig.html', adminno=adminno, date=date, lockerno=lockerno)




@app.route('/lockeradmin')
def lockeradmin():
    db_read = shelve.open("storage.db", "r")
    lockers = db_read['locker']
    list = []
    for id in lockers:
        list.append(lockers.get(id))
    db_read.close()
    return render_template('lockerAdmin.html', lockers=list)

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
                        resp.set_cookie('admin_no', admin_no)
                        resp.set_cookie('name',user_storage_name)
                        # key and value
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
            userz = User(admin_no,password,email,name,school,'student',course_name,pem_class)
            if userlist != {}:
                db_read2 = shelve.open("user.db", "r")
                user = db_read2["users"]

                for checking in user:
                    user_storage = (user.get(checking))
                    user_storage_admin_no = user_storage.get_admin_no()

                    if admin_no == user_storage_admin_no:
                        flash('You already have an account', 'danger')
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
            #first name put in admin_no second as name
            userz = Admin(name,password, email, name, school,'teacher')
            if userlist != {}:
                db_read2 = shelve.open("user.db", "r")
                user = db_read2["users"]

                for checking in user:
                    user_storage = (user.get(checking))
                    user_storage_name = user_storage.get_name()

                    if name ==user_storage_name:
                        flash('You already have an account', 'danger')
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
  ##REMEMBER TO PUT THE FOR LOOP OF SELECT FIELD INSDIE HERE
class LoopTeachers(object):
    def __iter__(self):
        db_read = shelve.open("user.db")
        try:
            userlist = db_read["users"]
        except:
            userlist = {}

        for user in userlist:
            user_storage = (userlist.get(user))

            if user_storage.get_identity()=='teacher':
                user_storage_name = user_storage.get_name()

                pair = (user_storage_name, user_storage_name)
                yield pair



class Booking_teachers_form(Form):
    name = SelectField('Name',
                       choices=LoopTeachers(),
                       )
    info = TextAreaField('Description', [validators.DataRequired()])
    time = SelectField('Time slot:  ', [validators.DataRequired()],
                       choices=[('', 'Select'), ('0810-0910', '0810-0910'), ('0900-0950', '0900-0950'),
                                ('1010-1100', '1010-1100'), ('1110-1200', '1110-1200'), ('1205-1255', '1205-1255'),
                                ('1300-1350', '1300-1350'), ('1400-1450', '1400-1450'),
                                ('1510-1600', '1510-1600'), ('1610-1700', '1610-1700'), ('1710-1800', '1710-1800')],
                       default='')
    date = DateField('DateTime', [validators.DataRequired()])


@app.route('/create_booking_teacher', methods=['GET', 'POST'])
def create_booking_teacher():
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
        info=form.info.data
        book=Booking(name,date,time,info,request.cookies.get('name'))
        print(date)
        print(datetime.datetime.now())
        ##type invalid date
        if date < datetime.date.today():
            flash('You have chosen a past date','danger')
            return redirect(url_for('create_booking_teacher'))
        if bookinglist != {}:
            db_read2 = shelve.open("booking.db", "r")
            booking = db_read2["bookings"]

            for checking in booking:
                book_storage = (booking.get(checking))
                book_storage_name =  book_storage.get_name()
                book_storage_date = book_storage.get_date()
                book_storage_time = book_storage.get_time()
                if name == book_storage_name and date == book_storage_date and time == book_storage_time:
                    flash('Time slot has been booked, please try another time slot', 'danger')
                    return redirect(url_for('create_booking_teacher'))
                else:
                    pass
        dayofweek=datetime.date.isoweekday(date)
        print(dayofweek)
        if dayofweek==7:
            flash('Sunday is an invalid day', 'danger')
            return redirect(url_for('create_booking_teacher'))
        db_read3 = shelve.open("teacher_timetable.db", "r")
        try:
            timetablelist = db_read3[name]
        except:
            timetablelist = {}
        print(timetablelist)
        if timetablelist != {}:
            timetable = db_read3[name]
            print('jeez')
            for checking in timetable:
                if checking <= 6:
                    multiplyer = 1
                elif checking <= 12:
                    multiplyer = 2
                elif checking <= 18:
                    multiplyer = 3
                elif checking <= 24:
                    multiplyer = 4
                elif checking <= 30:
                    multiplyer = 5
                elif checking <= 36:
                    multiplyer = 6
                elif checking <= 42:
                    multiplyer = 7
                elif checking <= 48:
                    multiplyer = 8
                elif checking <= 54:
                    multiplyer = 9
                elif checking <= 60:
                    multiplyer = 10
                timetable_storage = (timetable.get(checking))
                timetable_storage_time = timetable_storage.get_time()
                if time == timetable_storage_time:
                    if dayofweek==1:  #check with dayofweek1*multiplyer
                        multiplied=1*multiplyer
                        timetable_storages = timetable.get(multiplied)
                        if timetable_storages.get_module_name() =='':
                            id = len(bookinglist) + 1
                            book.set_status('Pending')
                            book.set_pubid(id)
                            bookinglist[id] = book
                            db_read["bookings"] = bookinglist
                            db_read.close()
                            flash('Successfully booked!', 'success')
                            return redirect(url_for('viewtest2'))
                        else:
                            flash('Timeslot occupied, please try again!', 'danger')
                            return redirect(url_for('create_booking_teacher'))

                    elif dayofweek==2:
                        multiplied = 2 * multiplyer
                        timetable_storages = timetable.get(multiplied)
                        if timetable_storages.get_module_name() =='':
                            id = len(bookinglist) + 1
                            book.set_status('Pending')
                            book.set_pubid(id)
                            bookinglist[id] = book
                            db_read["bookings"] = bookinglist
                            db_read.close()
                            flash('Sucessfully booked!', 'success')
                            return redirect(url_for('viewtest2'))
                        else:
                            flash('Timeslot occupied please try again!', 'danger')
                            return redirect(url_for('create_booking_teacher'))

                    elif dayofweek==3:
                        multiplied = 3 * multiplyer
                        timetable_storages = timetable.get(multiplied)
                        if timetable_storages.get_module_name() =='':
                            id = len(bookinglist) + 1
                            book.set_status('Pending')
                            book.set_pubid(id)
                            bookinglist[id] = book
                            db_read["bookings"] = bookinglist
                            db_read.close()
                            flash('Successfully booked!', 'success')
                            return redirect(url_for('viewtest2'))
                        else:
                            flash('Timeslot occupied, please try again!', 'danger')
                            return redirect(url_for('create_booking_teacher'))
                    elif dayofweek==4:
                        multiplied = 4 * multiplyer
                        timetable_storages = timetable.get(multiplied)
                        if timetable_storages.get_module_name() =='':
                            id = len(bookinglist) + 1
                            book.set_status('Pending')
                            book.set_pubid(id)
                            bookinglist[id] = book
                            db_read["bookings"] = bookinglist
                            db_read.close()
                            flash('Successfully booked!', 'success')
                            return redirect(url_for('viewtest2'))
                        else:
                            flash('Timeslot occupied, please try again!', 'danger')
                            return redirect(url_for('create_booking_teacher'))
                    elif dayofweek==5:
                        multiplied = 5 * multiplyer
                        timetable_storages = timetable.get(multiplied)
                        if timetable_storages.get_module_name() =='':
                            id = len(bookinglist) + 1
                            book.set_status('Pending')
                            book.set_pubid(id)
                            bookinglist[id] = book
                            db_read["bookings"] = bookinglist
                            db_read.close()
                            flash('Successfully booked!', 'success')
                            return redirect(url_for('viewtest2'))
                        else:
                            flash('Timeslot occupied, please try again!', 'danger')
                            return redirect(url_for('create_booking_teacher'))
                    elif dayofweek==6:
                        multiplied = 6 * multiplyer
                        timetable_storages = timetable.get(multiplied)
                        if timetable_storages.get_module_name() =='':
                            id = len(bookinglist) + 1
                            book.set_status('Pending')
                            book.set_pubid(id)
                            bookinglist[id] = book
                            db_read["bookings"] = bookinglist
                            db_read.close()
                            flash('Successfully booked!', 'success')
                            return redirect(url_for('viewtest2'))
                        else:
                            flash('Timeslot occupied, please try again!', 'danger')
                            return redirect(url_for('create_booking_teacher'))
                    elif dayofweek==7:
                        multiplied = 7 * multiplyer
                        timetable_storages = timetable.get(multiplied)
                        if timetable_storages.get_module_name() =='':
                            id = len(bookinglist) + 1
                            book.set_status('Pending')
                            book.set_pubid(id)
                            bookinglist[id] = book
                            db_read["bookings"] = bookinglist
                            db_read.close()
                            flash('Successfully booked!', 'success')
                            return redirect(url_for('viewtest2'))
                        else:
                            flash('Timeslot occupied ,please try again!', 'danger')
                            return redirect(url_for('create_booking_teacher'))

    return render_template('booking.html', form=form)

@app.route('/accept_booking/<int:id>', methods=['POST'])
def accept_booking(id):
    db_read = shelve.open("booking.db")
    try:
        bList = db_read["bookings"]
    except:
        bList= []
    try:
        print("id, ", id)
        book_storage = (bList.get(id))
        book_storage.set_status('Accepted')

        db_read["bookings"] = bList

        db_read.close()

        flash('Booking Accepted', 'success')

        return redirect(url_for('teacherbooking'))
    except:
        flash('Error in booking acception', 'danger')
        return redirect(url_for('teacherbooking'))

@app.route('/reject_booking/<int:id>', methods=['POST'])
def reject_booking(id):
    db_read = shelve.open("booking.db")
    try:
        bList = db_read["bookings"]
    except:
        bList = {}

    try:
        print("id, ", id)
        book_storage = (bList.get(id))
        book_storage.set_status('Rejected')
        db_read["bookings"] = bList
        db_read.close()
        flash('Booking Rejected', 'success')
        return redirect(url_for('teacherbooking'))

    except:
        flash('Error in booking rejection', 'danger')
        return redirect(url_for('teacherbooking'))

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
        bookingz= booking.get(pubid)
        if bookingz.get_status()!= 'Accepted' or bookingz.get_status()!='Rejected':
            list.append(booking.get(pubid))

    db_read.close()

    return render_template('view_all_bookings_teacher.html', bookings=list)

@app.route('/viewtest2')
def viewtest2():
    form = BookingStatusForm(request.form)
    db_read = shelve.open("booking.db")

    try:
        booking = db_read["bookings"]
    except:
        booking = {}

    print(booking)
    print('Hello')
    list3=[]

    for pubid in booking:
        list3.append(booking.get(pubid))
    print(list3)
    return render_template('view_all_bookings_forstudents.html', booking=list3, form=form)


class BookingStatusForm(Form):
    pubtype = SelectField('Booking Status', choices=[('confirm', 'confirm'), ('reject', 'reject'),('pending','pending')], default='pending')

@app.route('/teacher_timetable',methods=('GET', 'POST'))
def teacher_timetable():
    db_read = shelve.open("teacher_timetable.db")
    try:
        timetablelist = db_read[request.cookies.get('admin_no')]
    except:
        timetablelist = {}

    db_read2=shelve.open('timetable.db')
    try:
        database=db_read2['timetablez']
    except:
        database={}

    if timetablelist == {}:
        print(timetablelist)
        for game in range(1, 61):
            if game <= 6:
                timetablez = Teacher_timetable('', '', '', '', '', request.cookies.get('admin_no'),'0810-0910')
                timetablez.set_id(game)
                timetablelist[game] = timetablez
                db_read[request.cookies.get('admin_no')] = timetablelist
            elif game<=12:
                timetablez = Teacher_timetable('', '', '', '', '', request.cookies.get('admin_no'),'0900-0950')
                timetablez.set_id(game)
                timetablelist[game] = timetablez
                db_read[request.cookies.get('admin_no')] = timetablelist
            elif game <= 18:
                timetablez = Teacher_timetable('', '', '', '', '', request.cookies.get('admin_no'), '1010-1100')
                timetablez.set_id(game)
                timetablelist[game] = timetablez
                db_read[request.cookies.get('admin_no')] = timetablelist
            elif game <= 24:
                timetablez = Teacher_timetable('', '', '', '', '', request.cookies.get('admin_no'), '1110-1200')
                timetablez.set_id(game)
                timetablelist[game] = timetablez
                db_read[request.cookies.get('admin_no')] = timetablelist
            elif game<=30:
                timetablez = Teacher_timetable('', '', '', '', '', request.cookies.get('admin_no'), '1205-1255')
                timetablez.set_id(game)
                timetablelist[game] = timetablez
                db_read[request.cookies.get('admin_no')] = timetablelist
            elif game<=36:
                timetablez = Teacher_timetable('', '', '', '', '', request.cookies.get('admin_no'), '1300-1350')
                timetablez.set_id(game)
                timetablelist[game] = timetablez
                db_read[request.cookies.get('admin_no')] = timetablelist
            elif game<=42:
                timetablez = Teacher_timetable('', '', '', '', '', request.cookies.get('admin_no'), '1400-1450')
                timetablez.set_id(game)
                timetablelist[game] = timetablez
                db_read[request.cookies.get('admin_no')] = timetablelist
            elif game<=48:
                timetablez = Teacher_timetable('', '', '', '', '', request.cookies.get('admin_no'), '1510-1600')
                timetablez.set_id(game)
                timetablelist[game] = timetablez
                db_read[request.cookies.get('admin_no')] = timetablelist
            elif game<=54:
                timetablez = Teacher_timetable('', '', '', '', '', request.cookies.get('admin_no'), '1610-1700')
                timetablez.set_id(game)
                timetablelist[game] = timetablez
                db_read[request.cookies.get('admin_no')] = timetablelist
            elif game<=60:
                timetablez = Teacher_timetable('', '', '', '', '', request.cookies.get('admin_no'), '1710-1800')
                timetablez.set_id(game)
                timetablelist[game] = timetablez
                db_read[request.cookies.get('admin_no')] = timetablelist


#---------------------------------- START
#----------------------------------
#----------------------------------

    count = 1
    if request.method == 'POST':
        try:
            print('hi')
            file=request.files['file']
            print(file)
            print('test')
            file_name = secure_filename(file.filename)
            print(file_name)
            file.save(os.path.join(app.config['UPLOADS_PATH'],file_name))
        except:
            print(app.config['UPLOADS_PATH'])
            file = None
        test_file = open(file_name, 'r')

        for lines in test_file:
            print(lines)
            if lines=='':
                print('knnccb')
            linez = lines.split(',')
            if lines[0] != '-':
                if count <= 6:
                    timetablez = Teacher_timetable(linez[0], linez[1], linez[2], linez[3], linez[4],
                                                   request.cookies.get('admin_no'), '0810-0910')
                    timetablez.set_id(count)
                    timetablelist[count] = timetablez
                    db_read[request.cookies.get('admin_no')] = timetablelist
                    count += 1
                elif count<=12:
                    timetablez = Teacher_timetable(linez[0], linez[1], linez[2], linez[3], linez[4],
                                                   request.cookies.get('admin_no'), '0900-0950')
                    timetablez.set_id(count)
                    timetablelist[count] = timetablez
                    db_read[request.cookies.get('admin_no')] = timetablelist
                    count += 1
                elif count <= 18:
                    timetablez = Teacher_timetable(linez[0], linez[1], linez[2], linez[3], linez[4],
                                                   request.cookies.get('admin_no'), '1010-1100')
                    timetablez.set_id(count)
                    timetablelist[count] = timetablez
                    db_read[request.cookies.get('admin_no')] = timetablelist
                    count += 1
                elif count <= 24:
                    timetablez = Teacher_timetable(linez[0], linez[1], linez[2], linez[3], linez[4],
                                                   request.cookies.get('admin_no'), '1110-1200')
                    timetablez.set_id(count)
                    timetablelist[count] = timetablez
                    db_read[request.cookies.get('admin_no')] = timetablelist
                    count += 1
                elif count<=30:
                    timetablez = Teacher_timetable(linez[0], linez[1], linez[2], linez[3], linez[4],
                                                   request.cookies.get('admin_no'), '1205-1255')
                    timetablez.set_id(count)
                    timetablelist[count] = timetablez
                    db_read[request.cookies.get('admin_no')] = timetablelist
                    count += 1
                elif count<=36:
                    timetablez = Teacher_timetable(linez[0], linez[1], linez[2], linez[3], linez[4],
                                                   request.cookies.get('admin_no'), '1300-1350')
                    timetablez.set_id(count)
                    timetablelist[count] = timetablez
                    db_read[request.cookies.get('admin_no')] = timetablelist
                    count += 1
                elif count<=42:
                    timetablez = Teacher_timetable(linez[0], linez[1], linez[2], linez[3], linez[4],
                                                   request.cookies.get('admin_no'), '1400-1450')
                    timetablez.set_id(count)
                    timetablelist[count] = timetablez
                    db_read[request.cookies.get('admin_no')] = timetablelist
                    count += 1
                elif count<=48:
                    timetablez = Teacher_timetable(linez[0], linez[1], linez[2], linez[3], linez[4],
                                                   request.cookies.get('admin_no'), '1510-1600')
                    timetablez.set_id(count)
                    timetablelist[count] = timetablez
                    db_read[request.cookies.get('admin_no')] = timetablelist
                    count += 1
                elif count<=54:
                    timetablez = Teacher_timetable(linez[0], linez[1], linez[2], linez[3], linez[4],
                                                   request.cookies.get('admin_no'), '1610-1700')
                    timetablez.set_id(count)
                    timetablelist[count] = timetablez
                    db_read[request.cookies.get('admin_no')] = timetablelist
                    count += 1
                elif count<=60:
                    timetablez = Teacher_timetable(linez[0], linez[1], linez[2], linez[3], linez[4],
                                                   request.cookies.get('admin_no'), '1710-1800')
                    timetablez.set_id(count)
                    timetablelist[count] = timetablez
                    db_read[request.cookies.get('admin_no')] = timetablelist
                    count += 1
            else:
                print('hi')
                if count <= 6:
                    timetablez = Teacher_timetable('', '', '', '', '',
                                                   request.cookies.get('admin_no'), '0810-0910')
                    timetablez.set_id(count)
                    timetablelist[count] = timetablez
                    db_read[request.cookies.get('admin_no')] = timetablelist
                    count += 1
                elif count <= 12:
                    timetablez = Teacher_timetable('', '', '', '', '',
                                                   request.cookies.get('admin_no'), '0900-0950')
                    timetablez.set_id(count)
                    timetablelist[count] = timetablez
                    db_read[request.cookies.get('admin_no')] = timetablelist
                    count += 1
                elif count <= 18:
                    timetablez = Teacher_timetable('', '', '', '', '',
                                                   request.cookies.get('admin_no'), '1010-1100')
                    timetablez.set_id(count)
                    timetablelist[count] = timetablez
                    db_read[request.cookies.get('admin_no')] = timetablelist
                    count += 1
                elif count <= 24:
                    timetablez = Teacher_timetable('', '', '', '', '',
                                                   request.cookies.get('admin_no'), '1110-1200')
                    timetablez.set_id(count)
                    timetablelist[count] = timetablez
                    db_read[request.cookies.get('admin_no')] = timetablelist
                    count += 1
                elif count <= 30:
                    timetablez = Teacher_timetable('', '', '', '', '',
                                                   request.cookies.get('admin_no'), '1205-1255')
                    timetablez.set_id(count)
                    timetablelist[count] = timetablez
                    db_read[request.cookies.get('admin_no')] = timetablelist
                    count += 1
                elif count <= 36:
                    timetablez = Teacher_timetable('', '', '', '', '',
                                                   request.cookies.get('admin_no'), '1300-1350')
                    timetablez.set_id(count)
                    timetablelist[count] = timetablez
                    db_read[request.cookies.get('admin_no')] = timetablelist
                    count += 1
                elif count <= 42:
                    timetablez = Teacher_timetable('', '', '', '', '',
                                                   request.cookies.get('admin_no'), '1400-1450')
                    timetablez.set_id(count)
                    timetablelist[count] = timetablez
                    db_read[request.cookies.get('admin_no')] = timetablelist
                    count += 1
                elif count <= 48:
                    timetablez = Teacher_timetable('', '', '', '', '',
                                                   request.cookies.get('admin_no'), '1510-1600')
                    timetablez.set_id(count)
                    timetablelist[count] = timetablez
                    db_read[request.cookies.get('admin_no')] = timetablelist
                    count += 1
                elif count <= 54:
                    timetablez = Teacher_timetable('', '', '', '', '',
                                                   request.cookies.get('admin_no'), '1610-1700')
                    timetablez.set_id(count)
                    timetablelist[count] = timetablez
                    db_read[request.cookies.get('admin_no')] = timetablelist
                    count += 1
                elif count <= 60:
                    timetablez = Teacher_timetable('', '', '', '', '',
                                                   request.cookies.get('admin_no'), '1710-1800')
                    timetablez.set_id(count)
                    timetablelist[count] = timetablez
                    db_read[request.cookies.get('admin_no')] = timetablelist
                    count += 1
        return redirect(url_for('teacher_timetable', filename=file_name))


    print(count)
#---------------------------- END
#----------------------------
#----------------------------
    print(timetablelist)
    list = []
    for id in timetablelist:
        list.append(timetablelist.get(id))
    count=0
    return render_template('teacher_timetable3.html',list=list)

@app.route('/create_teacher_timetable/<int:id>', methods=('GET', 'POST'))
def create_teacher_timetable(id):
    form = Teacher_timetableForm(request.form)
    db_read = shelve.open("teacher_timetable.db")
    try:
        timetable = db_read[request.cookies.get('admin_no')]
    except:
        timetable = {}
    if request.method == 'POST':
        module_name = form.module_name.data
        block = form.block.data
        room=form.room.data
        school=form.school.data
        lesson_type=form.lesson_type.data
        if id<=6:
            timetablez=Teacher_timetable(module_name,block,room,school,lesson_type,
                                         request.cookies.get('admin_no'),'0810-0910')
        elif id <= 12:
            timetablez = Teacher_timetable(module_name, block, room, school, lesson_type,
                                           request.cookies.get('admin_no'), '0900-0950')
        elif id <= 18:
            timetablez = Teacher_timetable(module_name, block, room, school, lesson_type,
                                           request.cookies.get('admin_no'), '1010-1100')
        elif id <= 24:
            timetablez = Teacher_timetable(module_name, block, room, school, lesson_type,
                                           request.cookies.get('admin_no'), '1110-1200')
        elif id <= 30:
            timetablez = Teacher_timetable(module_name, block, room, school, lesson_type,
                                           request.cookies.get('admin_no'), '1205-1255')
        elif id <= 36:
            timetablez = Teacher_timetable(module_name, block, room, school, lesson_type,
                                           request.cookies.get('admin_no'), '1300-1350')
        elif id <= 42:
            timetablez = Teacher_timetable(module_name, block, room, school, lesson_type,
                                           request.cookies.get('admin_no'), '1400-1450')
        elif id <= 48:
            timetablez = Teacher_timetable(module_name, block, room, school, lesson_type,
                                           request.cookies.get('admin_no'), '1510-1600')
        elif id <= 54:
            timetablez = Teacher_timetable(module_name, block, room, school, lesson_type,
                                           request.cookies.get('admin_no'), '1610-1700')
        elif id <= 60:
            timetablez = Teacher_timetable(module_name, block, room, school, lesson_type,
                                           request.cookies.get('admin_no'), '1710-1800')

        timetablez.set_id(id)
        timetable[id] = timetablez
        db_read[request.cookies.get('admin_no')] = timetable

        db_read.close()
        flash('Successfully updated!', 'success')

        return redirect(url_for('teacher_timetable'))

    return render_template('create_teacher_timetable.html',form=form)


class Teacher_timetableForm(Form):
    module_name = StringField('Module Name')
    block = StringField('Block', [validators.DataRequired()])
    room=StringField('Room',[validators.DataRequired()])
    school = SelectField('School',[validators.DataRequired()],
                         choices=[('', 'Select'),('SIT', 'SIT'),('SCL', 'SCL'),('SBM', 'SBM'),
                                 ('SIDM', 'SIDM'),('SEG', 'SEG'),('SHSS', 'SHSS'), ('SDM', 'SDM')
                                ], default=' ' )
    lesson_type = SelectField('Lesson Type',
                     choices=[('Lecture', 'Lecture'), ('Practical', 'Practical'),('Tutorial','Tutorial')], default='Tutorial')



@app.route('/view_all_teacher_timetable',methods=('GET', 'POST'))
def view_all_teacher_timetable():
    db_read = shelve.open("teacher_timetable.db")
    list = []
    for id in db_read:
        print(id)
        try:
            timetablelist = db_read[id]
        except:
            timetablelist = {}
        print(timetablelist)
        list.append(id)
    print('===')
    print(list)
    return render_template('view_timetable.html',list=list)

@app.route('/view_teacher_timetable/<teacherid>', methods=('GET', 'POST'))
def view_teacher_timetable(teacherid):
    db_read = shelve.open("teacher_timetable.db")
    print(teacherid)
    try:
        timetablelist = db_read[teacherid]
    except:
        timetablelist = {}

    print(timetablelist)
    list = []
    for cell in timetablelist:
        list.append(timetablelist.get(cell))
    print(teacherid)
    return render_template('view_indivdual_timetable.html',list=list, teacher=teacherid)


@app.route('/assignments_student/<filename>')
def uploaded_filez(filename):
    return send_from_directory(app.config['UPLOADS_PATH'], filename)


def allowed_filesz(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class PhotoForm(Form):
    photo = FileField(validators=[''])


class CreateAssignments:
    def __init__(self, course, group, date, des, maxmarks, givenmarks):
        self.__course = course
        self.__group = group
        self.__date = date
        self.__des = des
        self.__maxmarks = maxmarks
        self.__id = ''
        self.__givenmarks = givenmarks

    def get_course(self):
        return self.__course

    def get_group(self):
        return self.__group

    def get_date(self):
        return self.__date

    def get_des(self):
        return self.__des

    def get_id(self):
        return self.__id

    def get_maxmarks(self):
        return self.__maxmarks

    def get_givenmarks(self):
        return self.__givenmarks

    def set_course(self, course):
        self.__course = course

    def set_group(self, group):
        self.__group = group

    def set_date(self, date):
        self.__date = date

    def set_id(self, id):
        self.__id = id

    def set_des(self, des):
        self.__des = des

    def set_maxmarks(self, maxmarks):
        self.__maxmarks = maxmarks

    def get_givenmark(self, givenmarks):
        self.__givenmarks = givenmarks


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class FormStuff(Form):
    selection = SelectField('Course/Module', [validators.DataRequired()],
                            choices=[('DIT/Programming Essentials', 'DIT/Programming Essentials'),
                                     ('DIT/Object-Oriented Programming and Project',
                                      'DIT/Object-Oriented Programming and Project'),
                                     ('DIT/Digital Media Interactive Design',
                                      'DIT/Digital Media Interactive Design'),
                                     ('DIT/Communication Skills', 'DIT/Communication Skills'),
                                     ('DCS/Data Communication and Networking',
                                      'DCS/Data Communication and Networking')]
                            )

    choice = MultiCheckboxField('Group', [validators.DataRequired()],
                                choices=[('IT1801', 'IT1801'), ('IT1802', 'IT1802'), ('IT1803', 'IT1803'),
                                         ('IT1804', 'IT1804'), ('IT1805', 'IT1805')],
                                )

    des = TextAreaField('Describe Task', [validators.DataRequired()])

    marks = StringField('Max mark for students', [validators.DataRequired])

    givenmarks = StringField('', [validators.DataRequired])


@app.route('/assignments_teacher', methods=['GET', 'POST'])
def assignt():
    form = FormStuff(request.form)
    db_read = shelve.open("dates.db")
    try:
        dateslist = db_read["users"]
    except:
        dateslist = {}
        print(dateslist)
    if request.method == 'POST':
        selection = request.form['selection']
        choice = form.choice.data
        date = request.form['daterange']
        des = request.form['des']
        maxmarks = request.form['marks']
        overall = CreateAssignments(selection, choice, date, des, maxmarks, '')
        id = len(dateslist) + 1
        overall.set_id(id)
        dateslist[id] = overall
        db_read["users"] = dateslist
        db_read.close()

        flash('You have uploaded the assignment.', 'success')
        return redirect(url_for('viewassignments'))

    return render_template('AssignmentsPgTeacher.html', form=form)


class FileUp:
    def __init__(self, file):
        self.__file = file
        self.__id = ''

    def get_file(self):
        return self.__file

    def get_id(self):
        return self.__id

    def set_file(self, file):
        self.__file = file

    def set_id(self, id):
        self.__id = id


@app.route('/assignments_student', methods=['GET', 'POST'])
def add_file():
    form = FormStuff(request.form)
    db_read = shelve.open("submissions.db", flag='c')
    try:
        submissionsList = db_read["submissions"]
    except:
        submissionsList = {}
    if request.method == "POST":
        try:
            file = request.files['file']
            file_name = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOADS_PATH'], file_name))
        except:
            file = None
        fileup = FileUp(file_name)
        id1 = len(submissionsList) + 1
        fileup.set_id(id1)
        submissionsList[id1] = fileup
        db_read["submissions"] = submissionsList

        db_read.close()

        flash('Submission uploaded', 'success')

        return redirect(url_for('viewassignmentsS', filename=file_name))

    return render_template('AsssignmentsPgStudents.html', form=form)


@app.route('/allassignments', methods=('GET', 'POST'))
def viewassignments():
    db_read = shelve.open('dates.db')
    list = []

    try:
        marksList = db_read['users']
    except:
        marksList = {}
    print('--------')
    print(list)
    for id in marksList:
        print(id)
        list.append(marksList.get(id))

    return render_template("ViewAssignments.html", list=list)


@app.route('/allassignmentsS', methods=('GET', 'POST'))
def viewassignmentsS():
    db_read = shelve.open('dates.db')
    list = []

    try:
        marksList = db_read['users']
    except:
        marksList = {}
    print('--------')
    print(list)
    for id in marksList:
        print(id)
        list.append(marksList.get(id))

    return render_template("ViewAssignmentsS.html", list=list)


@app.route('/individualassignments/<int:assignmentsid>', methods=('GET', 'POST'))
def individualassignments(assignmentsid):
    form = FormStuff(request.form)
    db_read = shelve.open('dates.db')
    try:
        assignmentsidList = db_read['users']
    except:

        assignmentsidList = []

    print(assignmentsid)
    if request.method == 'POST':
        assignmentzz = assignmentsidList.get(assignmentsid)
        selection = assignmentzz.get_course()
        choice = assignmentzz.get_group()
        date = assignmentzz.get_date()
        des = assignmentzz.get_des()
        maxmarks = assignmentzz.get_maxmarks()
        givenmarks = form.givenmarks.data
        overall = CreateAssignments(selection, choice, date, des, maxmarks, givenmarks)
        print(choice)
        print(date)
        overall.set_id(assignmentsid)
        assignmentsidList[assignmentsid] = overall
        db_read["users"] = assignmentsidList

    list2 = []
    list2.append(assignmentsidList.get(assignmentsid))

    return render_template('view_individual_assignments.html', form=form, list2=list2)



if __name__ == '__main__':
    app.run()


