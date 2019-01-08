from wtforms import *
import shelve


class CheckAvailForm(Form):
    dateav = DateField('Date Availability', format='%Y-%m-%d')
    locationav = SelectField('Locker Location', choices=[("SIT", "School of Information Technology"),
                                                       ("SBM", "School of Business Management"),
                                                       ("SCL", "School of Chemical and Life Sciences")])


class LockerForm(Form):
    #db_read = shelve.open("storage.db", "r")
    #lockerNos = db_read['locker']
    #dateData = form.date.data
    #kv = lockerNos.dateData
    adminno = StringField('Admin Number:* ', )
    date = DateField('Date:* ', format='%Y-%m-%d')
    location = SelectField('Locker Location: ', choices=[("SIT", "School of Information Technology"),
                                                       ("SBM", "School of Business Management"),
                                                       ("SCL", "School of Chemical and Life Sciences")])
    size = SelectField('Locker Size: ', choices=[("small", "Small"), ("medium", "Medium"), ("big", "Big")])
    lockerno = SelectField('Locker Number: ', choices=[("","")])

