from flask import Flask, render_template, request, flash, redirect, url_for, session
from wtforms import Form, StringField, validators, DateField, SelectField, SubmitField
from Locker import Locker
import shelve
from Forms import *
import tkinter
from tkinter import messagebox


app = Flask(__name__)
app.secret_key = 'secretkey'

@app.route('/CheckAvail')
def checkAvail():
    cform = CheckAvailForm(request.form)

    dateav = cform.dateav.data
    locationav = cform.locationav.data

    ##############
        #if

    ###############


    db_read = shelve.open("storage.db")

    try:
        lockerList = db_read["locker"]
    except:
        lockerList = {}

    if request.method == 'POST' and form.validate():
        pass

    return render_template("Locker_Public.html", form=form)


@app.route('/lockers', methods=['GET', 'POST'])
def func_locker():
    form = LockerForm(request.form)
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

    print(checkList)
    print(lockerList)

    if request.method == 'POST' or form.validate():
        date = form.date.data
        lockerno = request.form['lockernohtml']
        if checkList == {}:
            adminno = form.adminno.data
            date = form.date.data
            location = request.form['locationhtml']
            size = request.form['sizehtml']
            lockerno = request.form['lockernohtml']
            lockers = Locker(adminno, date, location, size, lockerno)
            id = len(lockerList) + 1
            lockers.set_id(id)
            lockerList[id] = lockers
            db_read["locker"] = lockerList
            db_read.close()
            #
            checkList[date] = []
            checkList[date].append(lockerno)
            db_readcheck["checklist"] = checkList
            db_readcheck.close()
            flash('Locker form submitted successfully!', 'success')
            # return redirect(url_for('func_locker'))
            print(1)
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
                    adminno = form.adminno.data
                    date = form.date.data
                    location = request.form['locationhtml']
                    size = request.form['sizehtml']
                    lockerno = request.form['lockernohtml']
                    lockers = Locker(adminno, date, location, size, lockerno)
                    id = len(lockerList) + 1
                    lockers.set_id(id)
                    lockerList[id] = lockers
                    db_read["locker"] = lockerList
                    db_read.close()
                    #
                    checkList[date] = []
                    checkList[date].append(lockerno)
                    db_readcheck["checklist"] = checkList
                    db_readcheck.close()
                    flash('Locker form submitted successfully!', 'success')
                    # return redirect(url_for('func_locker'))
                    print(2)
            else:
                adminno = form.adminno.data
                date = form.date.data
                location = request.form['locationhtml']
                size = request.form['sizehtml']
                lockerno = request.form['lockernohtml']
                lockers = Locker(adminno, date, location, size, lockerno)
                id = len(lockerList) + 1
                lockers.set_id(id)
                lockerList[id] = lockers
                db_read["locker"] = lockerList
                db_read.close()
                #
                checkList[date] = []
                checkList[date].append(lockerno)
                db_readcheck["checklist"] = checkList
                db_readcheck.close()
                flash('Locker form submitted successfully!', 'success')
                # return redirect(url_for('func_locker'))
                print(3)

            # for key, value in checkList.items():
            #     keyid = len(checkList)
            #     keyidcount = 0
            #     while keyid != keyidcount:
            #         if key == date:
            #             for ivalue in value:
            #                 if ivalue == lockerno:
            #                     # keyid = keyidcount
            #                     lockerRedirect(lockerno)
            #                     return redirect(url_for('func_locker'))
            #                 else:
            #                     keyidcount += 1
            #                     pass
            #         else:
            #             keyidcount += 1
            #             pass
            #     adminno = form.adminno.data
            #     date = form.date.data
            #     location = request.form['locationhtml']
            #     size = request.form['sizehtml']
            #     lockerno = request.form['lockernohtml']
            #     lockers = Locker(adminno, date, location, size, lockerno)
            #     id = len(lockerList) + 1
            #     lockers.set_id(id)
            #     lockerList[id] = lockers
            #     db_read["locker"] = lockerList
            #     db_read.close()
            #     #
            #     if date in checkList:
            #         checkList[date].append(lockerno)
            #         db_readcheck["checklist"] = checkList
            #         db_readcheck.close()
            #         flash('Locker form submitted successfully!', 'success')
            #         # return redirect(url_for('func_locker'))
            #     else:
            #         checkList[date] = []
            #         checkList[date].append(lockerno)
            #         db_readcheck["checklist"] = checkList
            #         db_readcheck.close()
            #         flash('Locker form submitted successfully!', 'success')
            #         # return redirect(url_for('func_locker'))

    return render_template('locker.html', form=form)

def lockerRedirect(lockerno):
    flash('Locker %s is already booked! Please enter another locker number.' % (lockerno),
          'warning')
    return redirect(url_for('func_locker'))


        # #####
        # lockerNosList = []
        #
        # if location == 'SIT':
        #     if size == 'small':
        #         lnlist = ['L01', 'L02']
        #         lockerNosList = lnlist
        #     elif size == 'medium':
        #         lnlist = ['L03']
        #         lockerNosList = lnlist
        #     elif size == 'big':
        #         lnlist = ['L04']
        #         lockerNosList = lnlist
        # elif location == 'SBM':
        #     if size == 'small':
        #         lnlist = ['B01', 'B02']
        #         lockerNosList = lnlist
        #     elif size == 'medium':
        #         lnlist = ['B03']
        #         lockerNosList = lnlist
        #     elif size == 'big':
        #         lnlist = ['B04']
        #         lockerNosList = lnlist
        # elif location == 'SCL':
        #     if size == 'small':
        #         lnlist = ['N01', 'N02']
        #         lockerNosList = lnlist
        #     elif size == 'medium':
        #         lnlist = ['N03']
        #         lockerNosList = lnlist
        #     elif size == 'big':
        #         lnlist = ['N04']
        #         lockerNosList = lnlist
        # else:
        #     pass
        #     # pls fill in alert

        #####



def checkalert():
    messagebox.showerror("Error", "This slot is already booked!")
    #print('''<script>
    #alert('Already Booked!');
    #</script>''')


class RequiredIf(object):

    def __init__(self, *args, **kwargs):
        self.conditions = kwargs
    def __call__(self, form, field):
        for name, data in self.conditions.items():
            if name not in form._fields:
                validators.Optional()(field)
                condition_field = form._fields.get(name)
            else:
                if condition_field.data == data:
                    validators.DataRequired().__call__(form, field)
                else:
                    validators.Optional().__call__(form, field)

@app.route('/payment')
def payment():
    return render_template('paypal.html', form=form)




@app.route('/')
def default():
    form = LockerForm(request.form)
    return render_template('locker.html', form=form)


#@app.route('/locker', methods=['GET', 'POST'])
#def new():
#    form = LockerForm(request.form)
#    cform = CheckForm(request.form)
#
#    db_read = shelve.open("storage.db")
#
#    try:
#        lockerList = db_read["locker"]
#    except:
#        lockerList = {}
#
#    dateav = cform.dateav.data
#
#    if request.method == 'POST' and form.validate():
#        for date in lockerList:
#            if dateav == date:
#                checkalert()
#            else:
#                    adminno = form.adminno.data
#                    date = form.date.data
#                    location = form.location.data
#                    size = form.size.data
#
#                    lockers = Locker(adminno, date, location, size)
#                    id = len(lockerList) + 1
#                    lockers.set_id(id)
#                    lockerList[id] = lockers
#                    db_read["locker"] = lockerList
#                    db_read.close()
#                    flash('Locker form submitted successfully!', 'success')
#                    return redirect(url_for('new'))
#    return render_template('locker.html', form=form)





#class LockerForm(Form):
#    adminno = StringField('Admin Number')
#    date = DateField('Date', format='%Y-%m-%d')
#    location = SelectField('Locker Location', choices=[("SIT", "School of Information Technology"),
#                                                       ("SBM", "School of Business Management"),
#                                                       ("SCL", "School of Chemical and Life Sciences")])
#    size = SelectField('Locker Size', choices=[("small", "Small"), ("medium", "Medium"), ("big", "Big")])
#
#class CheckForm(Form):
#    dateav = DateField('Date Availability', format='%Y-%m-%d')


@app.route('/lockeradmin')
def lockeradmin():
    db_read = shelve.open("storage.db", "r")
    lockers = db_read['locker']
    list = []
    for id in lockers:
        list.append(lockers.get(id))
    db_read.close()
    return render_template('lockerAdmin.html', lockers=list)
#PUT CHECK ON TOP



if __name__ == '__main__':
    app.run()
