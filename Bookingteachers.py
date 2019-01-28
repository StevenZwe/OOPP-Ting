
class Booking:
    def __init__(self,name,date,time,info,student_name):
        self.__name=name
        self.__date=date
        self.__time=time
        self.__student_name=student_name
        self.__info=info
        self.__pubid = ''
        self.__status=''

    def get_name(self):
        return self.__name

    def get_date(self):
        return self.__date

    def get_time(self):
        return self.__time

    def get_approval(self):
        return self.__approval

    def set_name(self,name):
        self.__name = name

    def set_date(self,date):
        self.__date = date

    def set_time(self,time):
        self.__time = time

    def set_approval(self,approval):
        self.__approval=approval

    def get_pubid(self):
        return self.__pubid

    def set_pubid(self, pubid):
        self.__pubid = pubid

    def get_newid(self):
        return self.__newid

    def set_newid(self, newid):
        self.__newid = newid

    def set_status(self,status):
        self.__status=status

    def get_status(self):
        return self.__status

    def set_student_name(self,student_name):
        self.__student_name=student_name

    def get_student_name(self):
        return self.__student_name

    def set_info(self,info):
        self.__info=info

    def get_info(self):
        return self.__info