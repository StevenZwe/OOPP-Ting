from flask import Flask, render_template, request, flash, redirect, url_for, session, send_from_directory
from wtforms import Form, StringField, TextAreaField, RadioField, SelectField, validators, PasswordField, FileField,\
    SelectMultipleField, widgets
from werkzeug.utils import secure_filename
import shelve
import os
from os.path import join, dirname, realpath

app = Flask(__name__)
app.secret_key = 'secret123'

UPLOAD_FOLDER = 'static\\documents\\'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_PATH'] = join(dirname(realpath(__file__)), 'static\\documents\\')


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
    def __init__(self, course, group, date, des, maxmarks):
        self.__course = course
        self.__group = group
        self.__date = date
        self.__des = des
        self.__maxmarks = maxmarks
        self.__id = ''

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


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class CourseOrModule(Form):
    selection = SelectField('Course/Module', [validators.DataRequired()],
                            choices=[('Information Technology/Programming Essentials',
                                      'Information Technology/Programming Essentials'),
                                     ('Information Technology/Object-Oriented Programming and Project',
                                      'Information Technology/Object-Oriented Programming and Project'),
                                     ('Information Technology/Digital Media Interactive Design',
                                      'Information Technology/Digital Media Interactive Design'),
                                     ('Information Technology/Communication Skills',
                                      'Information Technology/Communication Skills'),
                                     ('Info-Comm and Security/Data Communication and Networking',
                                      'Info-Comm and Security/Data Communication and Networking')]
                            )

    choice = MultiCheckboxField('Group', [validators.DataRequired()],
                                choices=[('Group1', 'Group1'), ('Group2', 'Group2'), ('Group3', 'Group3'),
                                         ('Group4', 'Group4'), ('Group5', 'Group5')],
                                )

    des = TextAreaField('Describe Task', [validators.DataRequired()])

    marks = StringField('Max mark for students', [validators.DataRequired])


@app.route('/assignments_teacher', methods=['GET', 'POST'])
def assignt():
    form = CourseOrModule(request.form)
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
        overall = CreateAssignments(selection, choice, date, des, maxmarks)
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

    def get_file(self):
        return self.__file

    def set_file(self, file):
        self.__file = file


@app.route('/assignments_student', methods=['GET', 'POST'])
def add_file():
    form = AddItems(request.form)

    if request.method == "POST" and form.validate():
        file_path = form.item_image.data
        file = request.files['file']
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == ' ':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_files(file.filename):
            filename = secure_filename(file.filename)
            basedir = os.path.abspath(os.path.dirname(__file__))

            print(app.config['UPLOADS_PATH'])
            print(filename)
            file.save(os.path.join(app.config['UPLOADS_PATH'], filename))
            file_path = UPLOAD_FOLDER + filename
            print(file_path)

        sub = FileUp(scourse, file_path)

        db_read = shelve.open("student_submission.db")

        try:
            student = db_read["users"]
        except:
            student = {}
            print(student)
        if request.method == 'POST':
            print('')
            scourse = request.form['course']
            file = request.form['file']
            overall = FileUp(file)
            print(overall)
            db_read["users"] = student
            db_read.close()
            print(overall)
    return render_template('AsssignmentsPgStudents.html')


class AddItems(Form):
    file = FileField('Describe the Task', [validators.DataRequired()])


#course/module, due date
# def upload(form):
#     if form.validate_on_submit():
#         f = form.photo.data
#         filename = secure_filename(f.filename)
#         f.save(os.path.join(
#             app.instance_path, 'photos', filename
#         ))
#         return redirect(url_for('index'))
#
#     return render_template('upload.html', form=form)
#

#dates = []

#sorted(dates, key=lambda d: map(int, d.split('-')))


@app.route('/allassignments')
def viewassignments():
    db_read = shelve.open("dates.db")
    try:
        dateslist = db_read["users"]
    except:
        dateslist = {}
    list = []
    for i in dateslist:
        list.append(dateslist.get(i))
    print(list)
    return render_template("ViewAssignments.html", dateslist=list)


class StudentMarks:
    def __init__(self, smarks):
        self.__smarks = smarks

    def get_smarks(self):
        return self.__smarks

    def set_marks(self, smarks):
        self.__smarks = smarks


@app.route('/marks')
def teachersmarking():
    form = StudentMarks(request.form)
    db_read = shelve.open("marks.db")
    try:
        markslist = db_read["users"]
    except:
        markslist = {}
        print(markslist)
    if request.method == 'POST':
        print('mark')
        studentmark = request.form['studentmark']
        overall = StudentMarks(studentmark)
        print(overall)
        db_read["users"] = markslist
        db_read.close()
        print(overall)

        flash("You have updated the student's marks.", 'success')
        return redirect(url_for('allassignments'))

    return render_template('TeacherMarking.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
