from flask import Flask, render_template, request, flash, redirect, url_for, session
from wtforms import Form, StringField, TextAreaField, RadioField, SelectField, validators, PasswordField
import shelve


app = Flask(__name__)
app.secret_key = 'secret123'


@app.route('/')
def default():
    return render_template('home.html')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/planner')
def planner():
    return render_template('planner.html')


@app.route('/assignments(teacher)', methods=['GET', 'POST'])
def assignt():
    form = CourseOrModule(request.form)
    return render_template('AssignmentsPgTeacher.html', form=form)


class CourseOrModule(Form):
    category = SelectField('Category', [validators.DataRequired()],
                           choices=[('', 'Select'), ('CM1', 'Course/Module1'), ('CM2', 'Course/Module2'),
                                    ('CM3', 'Course/Module3'), ('CM4', 'Course/Module4'), ('CM5', 'Course/Module5')],
                           default='')


#@app.route('/assignments(student)')
#def assigns():

if __name__ == '__main__':
    app.run()

