class Locker:
    def __init__(self, adminno, date, location, size, lockerno):
        self.__id = ''
        self.__adminno = adminno
        self.__date = date
        self.__location = location
        self.__size = size
        self.__lockerno = lockerno

    def get_id(self):
        return self.__id

    def set_id(self, id):
        self.__id = id

    def get_adminno(self):
        return self.__adminno

    def set_adminno(self, adminno):
        self.__adminno = adminno

    def get_date(self):
        return self.__date

    def set_date(self, date):
        self.__date = date

    def get_location(self):
        return self.__location

    def set_location(self, location):
        self.__location = location

    def get_size(self):
        return self.__size

    def set_size(self, size):
        self.__size = size

    def get_lockerno(self):
        return self.__lockerno

    def set_lockerno(self, lockerno):
        self.__lockerno = lockerno


