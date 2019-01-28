from flask import Flask, render_template, request, flash, redirect, url_for, session, send_from_directory
from wtforms import Form, StringField, TextAreaField, RadioField, SelectField, validators, PasswordField, FileField,\
    SelectMultipleField, widgets
from werkzeug.utils import secure_filename
import shelve
import os
from os.path import join, dirname, realpath

app = Flask(__name__)
app.secret_key = 'secret123'

UPLOAD_FOLDER = '/static/Documents/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOADS_PATH'] = join(dirname(realpath(__file__)), 'static\\Documents\\')


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOADS_PATH'], filename)


def allowed_files(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class PhotoForm(Form):
    photo = FileField(validators=[''])


@app.route('/')
def default():
    return render_template('home.html')


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
                                choices=[('Group1', 'Group1'), ('Group2', 'Group2'), ('Group3', 'Group3'),
                                         ('Group4', 'Group4'), ('Group5', 'Group5')],
                                )

    des = TextAreaField('Describe Task', [validators.DataRequired()])

    marks = StringField('Max mark for students', [validators.DataRequired])

    test = SelectField('Course/Module', [validators.DataRequired()],
                       choices=[('DIT/Programming Essentials', 'DIT/Programming Essentials'),
                                ('DIT/Object-Oriented Programming and Project',
                                'DIT/Object-Oriented Programming and Project'),
                                ('DIT/Digital Media Interactive Design',
                                'DIT/Digital Media Interactive Design'),
                                ('DIT/Communication Skills', 'DIT/Communication Skills'),
                                ('DCS/Data Communication and Networking',
                                'DCS/Data Communication and Networking')]
                       )

    givingmarks = StringField('', [validators.DataRequired])


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
        print('day')
        selection = request.form['selection']
        choice = form.choice.data
        date = request.form['daterange']
        des = request.form['des']
        maxmarks = request.form['marks']
        overall = CreateAssignments(selection, choice, date, des, maxmarks, '')
        print(overall)
        id = len(dateslist) + 1
        overall.set_id(id)
        dateslist[id] = overall
        db_read["users"] = dateslist
        db_read.close()
        print(overall)

        flash('You have uploaded the assignment.', 'success')
        return redirect(url_for('home'))

    return render_template('AssignmentsPgTeacher.html', form=form)


class FileUp:
    def __init__(self, scourse, file):
        self.__file = file
        self.__scourse = scourse
        self.__id = ''

    def get_file(self):
        return self.__file

    def get_scourse(self):
        return self.__scourse

    def get_id(self):
        return self.__id

    def set_file(self, file):
        self.__file = file

    def set_scourse(self, scourse):
        self.__scourse = scourse

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

    if request.method == "POST" and form.validate():
        test = form.test.data
        try:
            file = request.files['file']
            file_name = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOADS_PATH'], file_name))
        except:
            file = None

        fileup = FileUp(test, file_name)
        id1 = len(submissionsList) + 1
        fileup.set_id(id1)
        submissionsList[id1] = fileup
        db_read["submissions"] = submissionsList

        db_read.close()

        flash('Submission uploaded', 'success')

        return redirect(url_for('home', filename=file_name))

    return render_template('AsssignmentsPgStudents.html', form=form)


@app.route('/allassignments')
def viewassignments():
    # form = CreateAssignments(request.form)
    # db_read = shelve.open("dates.db")
    # try:
    #     dateslist = db_read["users"]
    # except:
    #     dateslist = {}
    # list = []
    # for i in dateslist:
    #     list.append(dateslist.get(i))
    # if request.method == "POST":
    #     selection = request.form['selection']
    #     choice = form.choice.data
    #     date = request.form['daterange']
    #     des = request.form['des']
    #     maxmarks = request.form['marks']
    #     givenmarks = request.form['givingmarks']
    #     overall = CreateAssignments(selection, choice, date, des, maxmarks, givenmarks)
    #     print(overall)
    # print(list)

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


@app.route('/individualassignments/<int:assignmentsid>', methods=('GET','POST'))
def individualassignments(assignmentsid):
    form = FormStuff(request.form)
    db_read = shelve.open('dates.db')
    try:
        assignmentsidList = db_read['users']
    except:
        assignmentsidList = []

    return render_template('view_individual_assignments.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
