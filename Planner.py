class Planner:
    def __init__(self, title, date, time, priority):
        self.__task = title
        self.__date = date
        self.__time = time
        self.__desc = ''
        self.__priority = priority

    def get_task(self):
        return self.__task

    def get_date(self):
        return self.__date

    def get_time(self):
        return self.__time

    def get_desc(self):
        return self.__desc

    def get_priority(self):
        return self.__priority

    def get_id(self):
        return self.__id

    def set_task(self,task):
        self.__task = task

    def set_date(self,date):
        self.__date = date

    def set_time(self,time):
        self.__time = time

    def set_desc(self,desc):
        self.__desc = desc

    def set_priority(self, priority):
        self.__priority = priority

    def set_id(self, id):
        self.__id = id

class Calendar():
    def __init__(self):
        self.title = ''
        self.start = ''
        self.allDay = ''
        self.color = ''
        self.id = ''

    def set_id(self,id):
        self.id = id

    def set_title(self,task):
        self.title = task

    def set_start(self,date):
        self.start = date

    def set_allDay(self):
        self.allDay = False

    def set_color(self,color):
        self.color = color
