from wtforms import Form,StringField,TextAreaField, RadioField, SelectField,validators

class User:
    def __init__(self, block, room_no, date, time):
        self.__block = block
        self.__room_no = room_no
        self.__date = date
        self.__time = time

    def get_block(self):
        return self.__block
    def get_room_no(self):
        return self.__room_no
    def get_date(self):
        return self.__date
    def get_time(self):
        return self.__time

    def set_block(self,block):
        self.__block = block

    def set_room_no(self,room_no):
        self.__room_no = room_no

    def set_date(self,date):
        self.__date = date

    def set_time(self,time):
        self.__time = time

class MyForm(Form):
    name = StringField('Name', [InputRequired()])

    def validate_name(form, field):
        if len(field.data) > 50:
            raise ValidationError('Name must be less than 50 characters')