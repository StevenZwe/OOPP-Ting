from wtforms import Field

class Booking:
    def __init__(self,blcok, room_no, date, time):
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


class MyForm(Form):
    name = StringField('Name', [InputRequired()])

    def validate_name(form, field):
        if len(field.data) > 50:
            raise ValidationError('Name must be less than 50 characters')