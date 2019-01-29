from flask import Flask, render_template, request, flash, redirect, url_for, session, \
    send_from_directory,make_response
from wtforms import Form, StringField, TextAreaField, RadioField, SelectField, validators, PasswordField, FileField,\
    SelectMultipleField, widgets
from werkzeug.utils import secure_filename
import shelve
import os
from os.path import join, dirname, realpath
import wget

app = Flask(__name__)
app.secret_key = 'secret123'

UPLOAD_FOLDER = '/static/Documents/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOADS_PATH'] = join(dirname(realpath(__file__)), 'static\\Documents\\')


@app.route('/assignments_student/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOADS_PATH'], filename)


def allowed_files(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class PhotoForm(Form):
    photo = FileField(validators=[''])


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
            # to check if database is empty or not, if is empty return as flash
            if userlist != {}:
                db_read2 = shelve.open("user.db", "r")
                user = db_read2["users"]

                for checking in user:
                    user_storage = (user.get(checking))
                    user_storage_admin_no = user_storage.get_admin_no()
                    user_storage_password = user_storage.get_password()
                    user_storage_name = user_storage.get_name()
                    user_storage_identity = user_storage.get_identity()
                    user_storage_userid = user_storage.get_userid()
                    if user_storage_admin_no != admin_no or user_storage_password != password:
                        if user_storage_identity == 'teacher' and user_storage_name==admin_no and user_storage_password==password:
                                session['id'] = admin_no
                                session['user_admin_No'] = admin_no
                                session['logged_in'] = True
                                session['identity'] = user_storage_identity
                                resp = make_response(redirect(url_for('home')))
                                resp.set_cookie('admin_no', admin_no)  #key and value
                                return resp
                    else:
                        session['id'] = user_storage_userid
                        session['user_admin_No'] = user_storage_admin_no
                        session['identity'] = user_storage_identity
                        session['logged_in'] = True
                        resp = make_response(redirect(url_for('home')))
                        resp.set_cookie('admin_no', admin_no)
                        resp.set_cookie('name', user_storage_name)
                        # key and value
                        return resp
                        return redirect(url_for('home'))

            flash('Wrong admin number or password', 'danger')
    return render_template('Login2.html')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/planner')
def planner():
    return render_template('planner.html')


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
        return redirect(url_for('home'))

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

        return redirect(url_for('home', filename=file_name))

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

    if request.method == '':
        url = 'http://i3.ytimg.com/vi/J---aiyznGQ/mqdefault.jpg'
        wget.download(url, '/Users/Courtney/Desktop/Organizer-Ting/static/Documents')
        print('Beginning file download with wget module')

    return render_template('view_individual_assignments.html', form=form, list2=list2)


if __name__ == '__main__':
    app.run(debug=True)
