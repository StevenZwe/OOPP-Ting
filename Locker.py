from wtforms import Form, StringField, DateField, SelectField, SubmitField
from wtforms import validators, ValidationError


class Rental(Form):
    adminno = StringField('Admin No.', [validators.Length(min=7, max=7)])
    date = DateField('Date', [validators.DataRequired("Please enter a date")])
    location = SelectField('Locker Location', choice=[("blka", "Block A"), ("blkl", "Block L"), ("blks", "Block S"),
                                                      ("blkk", "Block K"), ("blkb", "Block B")])
    size = SelectField('Locker Size', choice=[("small", "Small"), ("medium", "Medium"), ("big", "Big")])
    submit = SubmitField('Submit')

class Check(Form):
    dateav = DateField('Date')
    locationav = SelectField('Locker Location', choice=[("blka", "Block A"), ("blkl", "Block L"), ("blks", "Block S"),
                                                        ("blkk", "Block K"), ("blkb", "Block B")])
    submit = SubmitField('Check Availability')




















#class Rental(Form):
#    def __init__(self, adminno, date, location, size, submit):
#        self.__id = ''
#        self.__adminno = adminno
#        self.__date = date
#        self.__location = location
#        self.__size = size
#        self.__submit = submit
#
#    def get_adminno(self):
#        return self.__adminno
#
#    def get_date(self):
#        return self.__date
#
#    def get_location(self):
#        return self.__location
#
#    def get_size(self):
#        return self.__size
#
#    def get_submit(self):
#        return self.__submit
#
#    def set_adminno(self, adminno):
#        self.__adminno = adminno
#
#    def set_date(self, date):
#        self.__date = date
#
#    def set_location(self, location):
#        self.__location = location
#
#    def set_size(self, size):
#        self.__size = size
#
#    def set_submit(self, submit):
#        self.__submit = submit
#
#
#
#
#
#class Check(Form):
#    def __init__(self, dateav, locationav, submit):
#        self.__dateav = dateav
#        self.__locationav = locationav
#        self.__submit = submit
#
#    def get_dateav(self):
#        return self.__dateav
#
#    def get_locationav(self):
#        return self.__locationav
#
#    def get_submit(self):
#        return self.__submit
#
#    def set_locationav(self, locationav):
#        self.__locationav = locationav
#
#    def set_dateav(self, dateav):
#        self.__dateav = dateav
#
#    def set_submit(self, submit):
#        self.__submit = submit










#def storelocker():
 #   lockerobj = {}

#def lockertxtfile():
 #   rental_file = open('storelocker.txt','a')
  #  rental_file.close()








#@app.route('/lockers', methods=("GET", "POST"))
#def lockers():
#    form =
#    if request.method == "POST"
#        username = resuest.form['']





