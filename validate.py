
class Roombooking:
    def __init__(self, block, room_no, date,time,admin):
        self.__block = block
        self.__room_no = room_no
        self.__date = date
        self.__time = time
        self.__roomid = ''
        self.__admin = admin

    def get_block(self):
        return self.__block
    def get_room_no(self):
        return self.__room_no
    def get_date(self):
        return self.__date
    def get_time(self):
        return self.__time
    def get_roomid(self):
        return self.__roomid
    def get_admin(self):
        return self.__admin

    def set_block(self,block):
        self.__block = block

    def set_room_no(self,room_no):
        self.__room_no = room_no

    def set_date(self,date):
        self.__date = date

    def set_time(self,time):
        self.__time = time

    def set_room_id(self,roomid):
        self.__roomid = roomid

    def set_admin(self,admin):
        self.__admin = admin



