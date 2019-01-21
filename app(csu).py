from flask import Flask, render_template, request, flash, redirect, url_for, session, send_from_directory
from wtforms import Form, StringField, TextAreaField, RadioField, SelectField, validators, PasswordField, FileField,\
    SelectMultipleField
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


def allowed_files():
    return '.' in filename and \
            filename.rsplit('.', 1) [1].lower() in ALLOWED_EXTENSIONS


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


class TeacherSide:
    def __init__(self, course, group, date, des):
        self.__course = course
        self.__group = group
        self.__date = date
        self.__des = des
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
        choice = request.form['choice']
        date = request.form['daterange']
        des = request.form['des']
        overall = TeacherSide(selection, choice, date, des)
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


class CourseOrModule(Form):
    selection = SelectField('Category', [validators.DataRequired()],
                            choices=[('', 'Select'), ('Course/Module1', 'Course/Module1'),
                                     ('Course/Module2', 'Course/Module2'), ('Course/Module3', 'Course/Module3'),
                                     ('Course/Module4', 'Course/Module4'), ('Course/Module5', 'Course/Module5')],
                            default='')

    choice = SelectMultipleField('Category', [validators.DataRequired()],
                                 choices=[('', 'Select'), ('Class1', 'Class1'), ('Class2', 'Class2'),
                                          ('Class3', 'Class3'), ('Class4', 'Class4'), ('Class5', 'Class5')],
                                 default='')

    des = TextAreaField('Describe the Task', [validators.DataRequired()])


#class wtforms.fields.BooleanField(default field arguments):
#    Choice = SelectField('Category', [validators.DataRequired()],
#                         choices=[('', 'Select'), ('CM1', 'Course/Module1'), ('CM2', 'Course/Module2'),
#                                  ('CM3', 'Course/Module3'), ('CM4', 'Course/Module4'), ('CM5', 'Course/Module5')],
#                         default='')


class FileUp:
    def __init__(self, file):
        self.__file = file

    def get_file(self):
        return self.__file

    def set_file(self, newfile):
        self.__file = newfile


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
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            basedir = os.path.abspath(os.path.dirname(__file__))

            print(app.config['UPLOADS_PATH'])
            print(filename)
            file.save(os.path.join(app.config['UPLOADS_PATH'], filename))
            file_path = UPLOAD_FOLDER + filename
            print(file_path)

        sub = Submissions(scourse, file_path)

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
    list=[]
    for i in dateslist:
        list.append(dateslist.get(i))
    print(list)
    return render_template("ViewAssignments.html", dateslist=list)


if __name__ == '__main__':
    app.run(debug=True)
