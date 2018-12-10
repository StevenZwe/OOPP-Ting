from flask import Flask, render_template, request, flash, redirect, url_for, session
from wtforms import Form, StringField, TextAreaField, RadioField, SelectField, validators, PasswordField


app = Flask(__name__)


@app.route('/')
def default():
    return render_template('home.html')


@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/planner')
def planner():
    return render_template('planner.html')


if __name__ == '__main__':
    app.run()
  