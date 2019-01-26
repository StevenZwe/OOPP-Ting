from flask import Flask, render_template, request, flash, redirect, url_for, session
import shelve

class Teacher_timetable:
    def __init__(self,module_name,block,room,school,lesson_type,username,time):
        self.__module_name = module_name
        self.__block = block
        self.__room = room
        self.__school = school
        self.__lesson_type = lesson_type
        self.__id=''
        self.__username = username
        self.__time=time

    def get_module_name(self):
        return self.__module_name

    def get_block(self):
        return self.__block

    def get_room(self):
        return self.__room

    def get_school(self):
        return self.__school

    def get_lesson_type(self):
        return self.__lesson_type

    def set_module_name(self,module_name):
        self.__module_name = module_name

    def set_block(self,block):
        self.__block = block

    def set_room(self,room):
        self.__room = room

    def set_school(self,school):
        self.__school= school

    def set_lesson_type(self, lesson_type):
        self.__lesson_type = lesson_type

    def get_id(self):
        return self.__id

    def set_id(self, id):
        self.__id = id

    def get_username(self):
        return self.__username

    def set_username(self,username):
         self.__username=username

    def set_time(self,time):
        self.__time=time

    def get_time(self):
        return self.__time