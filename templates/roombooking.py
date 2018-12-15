from flask import Flask, render_template,request
from wtforms import Form, StringField,TextAreaField, RadioField, SelectField,validators

class PublicationForm(Form):


    Block = SelectField('block', choices=[('', 'Select'), ('SCL', 'P'), ('SBM', 'B'),
    ('SIDM', 'M'), ('SIT', 'L'), ('SEG', 'S')],
    default='')

    Room = SelectField('Room', choices=[('', 'Select'), ('Level 4', '432'), ('Level 5', '532'),
    ('Level 6', '604')], default='')

    Time = SelectField('Time', choices=[('', 'Select'), ('11:00', 'am'), ('11:30', 'am'),
                                          ('11:45', 'am')], default='')



    purpose = StringField('Purpose')