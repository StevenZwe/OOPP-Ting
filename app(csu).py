from flask import Flask, render_template, request, flash, redirect, url_for, session
from wtforms import Form, StringField, TextAreaField, RadioField, SelectField, validators, PasswordField, FileField, SelectMultipleField
from werkzeug.utils import secure_filename
import shelve

app = Flask(__name__)
app.secret_key = 'secret123'

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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
    def __init__(self, course, module, date, des):
        self.__course = course
        self.__module = module
        self.__date = date
        self.__des = des
        self.__id = ''

    def get_course(self):
        return self.__course

    def get_module(self):
        return self.__module

    def get_date(self):
        return self.__date

    def get_des(self):
        return self.__des

    def set_course(self, newcourse):
        self.__course = newcourse

    def set_module(self, newmodule):
        self.__module = newmodule

    def set_date(self, newdate):
        self.__date = newdate

    def get_id(self):
        return self.__id

    def set_id(self,newid):
        self.__id = newid

    def set_des(self,newdes):
        self.__id = newdes


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
                            choices=[('', 'Select'), ('CM1', 'Course/Module1'), ('CM2', 'Course/Module2'),
                                     ('CM3', 'Course/Module3'), ('CM4', 'Course/Module4'), ('CM5', 'Course/Module5')],
                            default='')

    choice = SelectMultipleField('Category', [validators.DataRequired()],
                         choices=[('', 'Select'), ('CL1', 'Class1'), ('CL2', 'Class2'),
                                  ('CL3', 'Class3'), ('CL4', 'Class4'), ('CL5', 'Class5')],
                         default='')

    des = TextAreaField('Describe the Task', [validators.DataRequired()])


#class wtforms.fields.BooleanField(default field arguments):
#    Choice = SelectField('Category', [validators.DataRequired()],
#                         choices=[('', 'Select'), ('CM1', 'Course/Module1'), ('CM2', 'Course/Module2'),
#                                  ('CM3', 'Course/Module3'), ('CM4', 'Course/Module4'), ('CM5', 'Course/Module5')],
#                         default='')


@app.route('/assignments_student', methods=['GET', 'POST'])
def assigns():
    return render_template('AssignmentsPgStudents.html')


def upload():
    if form.validate_on_submit():
        f = form.photo.data
        filename = secure_filename(f.filename)
        f.save(os.path.join(
            app.instance_path, 'photos', filename
        ))
        return redirect(url_for('index'))

    return render_template('upload.html', form=form)


dates = []

sorted(dates, key=lambda d: map(int, d.split('-')))


if __name__ == '__main__':
    app.run()
