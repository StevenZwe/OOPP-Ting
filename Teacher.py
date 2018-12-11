from wtforms import Form, StringField, TextAreaField, RadioField, SelectField, validators, PasswordField


class CourseOrModule(Form):
    category = SelectField('Caterory', [validators.DataRequired()],
                           choices=[('', 'Select'), ('CM1', 'Course/Module1'), ('CM2', 'Course/Module2'),
                                    ('CM3', 'Course/Module3'), ('CM4', 'Course/Module4'), ('CM5', 'Course/Module5')],
                           default='')