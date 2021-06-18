import datetime
from mongoengine import *
from course.models import Course
# Create your models here.
"""
用户实体类
"""


class Student(Document):
    uid = SequenceField(primary_key=True)  # 自增id ,主码
    username = StringField(max_length=12,unique=True,null=False,verbose_name='学号')
    name = StringField(max_length=20,verbose_name='姓名',default='')
    password = StringField(max_length=100,verbose_name='密码')
    email = EmailField(verbose_name='邮箱')
    sex = IntField(default=0,verbose_name='性别') # man 0,woman 1
    major = StringField(max_length=20,required=False,verbose_name='专业')
    phone = StringField(max_length=20)
    creat_time = StringField(max_length=50,verbose_name='创建时间',
                             default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    add_course = ListField(ReferenceField(Course))
    meta = {'collection': 'student'}  # 数据库中的集合


class Teacher(Document):
    uid = SequenceField(primary_key=True)  # 自增id ,主码
    username = StringField(max_length=12,unique=True,null=False,verbose_name='教工号')
    name = StringField(max_length=20,verbose_name='姓名')
    password = StringField(max_length=100,null=False)
    email = EmailField(verbose_name = '邮箱')
    phone = StringField(max_length=20)
    sex = IntField(default=0, verbose_name='性别')  # man 0,woman 1
    major = StringField(max_length=20, required=False, verbose_name='专业')
    creat_time = StringField(max_length=50, verbose_name='创建时间',
                             default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    meta = {'collection': 'teacher'}  # 数据库集合







