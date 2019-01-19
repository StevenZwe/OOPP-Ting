from flask import Flask, render_template, request, flash, redirect, url_for, session
from wtforms import Form, StringField, validators, DateField, SelectField, SubmitField
from Locker import Locker
import shelve
from Forms import *
import tkinter
from tkinter import *
from tkinter import messagebox
import time


app = Flask(__name__)
app.secret_key = 'secretkey'

@app.route('/CheckAvail')
def checkAvail():
    cform = CheckAvailForm(request.form)

    dateav = cform.dateav.data
    locationav = cform.locationav.data


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
    db_readordered = shelve.open("ordered.db")

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
        #if checklist is empty (no one booked anything)
        if checkList == {}:
            flash('Locker form submitted successfully!', 'success')
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
            #
            session['adminno'] = adminno
            session['date'] = date
            session['lockerno'] = lockerno
            #
            window = Tk()
            window.eval('tk::PlaceWindow %s center' % window.winfo_toplevel())
            window.withdraw()
            if messagebox.askyesno('Question', "You've made a reservation for %s on %s. Would you like to proceed "
                                               "to payment?" % (lockerno, date), icon = 'info') == True:
                return redirect(url_for('payment'))
            else:
                flash("You decide not to pay. Transaction and booking has been cancelled.", 'warning')
                return redirect(url_for('func_locker'))

            window.decoinify()
            window.destroy()
            window.quit()
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
                    flash('Locker form submitted successfully!', 'success')
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
                    #
                    session['adminno'] = adminno
                    session['date'] = date
                    session['lockerno'] = lockerno
                    #
                    window = Tk()
                    window.eval('tk::PlaceWindow %s center' % window.winfo_toplevel())
                    window.withdraw()
                    if messagebox.askyesno('Question',
                                           "You've made a reservation for %s on %s. Would you like to proceed "
                                           "to payment?" % (lockerno, date), icon='info') == True:
                        return redirect(url_for('payment'))
                    else:
                        flash("You decide not to pay. Transaction and booking has been cancelled.", 'warning')
                        return redirect(url_for('func_locker'))

                    window.decoinify()
                    window.destroy()
                    window.quit()
                    # return redirect(url_for('func_locker'))
                    print(2)
            else:
                flash('Locker form submitted successfully!', 'success')
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
                #
                session['adminno'] = adminno
                session['date'] = date
                session['lockerno'] = lockerno
                #
                window = Tk()
                window.eval('tk::PlaceWindow %s center' % window.winfo_toplevel())
                window.withdraw()
                if messagebox.askyesno('Question', "You've made a reservation for %s on %s. Would you like to proceed "
                                                   "to payment?" % (lockerno, date), icon='info') == True:
                    return redirect(url_for('payment'))
                else:
                    flash("You decide not to pay. Transaction and booking has been cancelled.", 'warning')
                    return redirect(url_for('func_locker'))

                window.decoinify()
                window.destroy()
                window.quit()
                # return redirect(url_for('func_locker'))
                print(3)

    return render_template('locker.html', form=form)

def lockerRedirect(lockerno):
    flash('Locker %s is already booked! Please enter another locker number.' % (lockerno),
          'warning')
    return redirect(url_for('func_locker'))




def checkalert():
    messagebox.showerror("Error", "This slot is already booked!")


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
    adminno = session.get('adminno', None)
    date = session.get('date', None)
    lockerno = session.get('lockerno', None)
    return render_template('paypal.html', adminno=adminno, date=date, lockerno=lockerno)




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


@app.route('/')
def default():
    form = LockerForm(request.form)
    return render_template('locker.html', form=form)



if __name__ == '__main__':
    app.run()
