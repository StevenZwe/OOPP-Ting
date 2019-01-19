import shelve
import uuid
from datetime import date
#name,admin_no,password,email,school,course_name,pem_class
class User:
    def __init__(self,admin_no,password,email,name,school,course_name,pem_class,identity):
        self.__userid =''
        self.__admin_no = admin_no
        self.__password = password
        self.__email=email
        self.__name=name
        self.__school=school
        self.__course_name=course_name
        self.__pem_class=pem_class
        self.__identity=identity

    def get_userid(self):
        return self.__userid

    def set_userid(self, userid):
        self.__userid=userid

    def set_admin_no(self, admin_no):
        self.__admin_no = admin_no

    def set_password(self, password):
        self.__password = password

    def set_email(self, email):
        self.__email = email

    def set_name(self, name):
        self.__name = name

    def set_school(self,school):
        self.__school=school

    def set_course_name(self,course_name):
        self.__course_name=course_name

    def set_pem_class(self,pem_class):
        self.__pem_class=pem_class


    def get_admin_no(self):
        return self.__admin_no

    def get_password(self):
        return self.__password

    def get_email(self):
        return self.__email

    def get_name(self):
        return self.__name

    def get_school(self):
        return self.__school

    def get_course_name(self):
        return self.__course_name

    def get_pem_class(self):
        return self.__pem_class


    def get_identity(self):
        return self.__identity

    def set_identity(self,identity):
        self.__identity=identity

