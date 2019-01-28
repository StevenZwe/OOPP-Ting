class Planner:
    def __init__(self,task,date,time,desc,priority):
        self.__task = task
        self.__date = date
        self.__time = time
        self.__desc = desc
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

    def set_task(self,task):
        self.__task = task

    def set_date(self,date):
        self.__date = date

    def set_time(self,time):
        self.__time = time

    def set_desc(self,desc):
        self.__desc= desc

    def set_priority(self, priority):
        self.__priority = priority

    def get_pubid(self):
        return self.__pubid

    def set_pubid(self, pubid):
        self.__pubid = pubid
