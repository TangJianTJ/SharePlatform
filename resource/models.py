import datetime
import os
from mongoengine import *
from course.models import Course
from user.models import Teacher
# Create your models here.
"""
资源实体类
"""


class Resource(Document):
    id = SequenceField(primary_key=True)  # 自增id
    name = StringField(max_length=100,default='资源标题')
    type = StringField(max_length=20,default='file',verbose_name='文件类型')
    upload_time = StringField(max_length=50, verbose_name='上传日期',
                              default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    owner = ReferenceField(Teacher)  # 上传资源的教师
    size = StringField(max_length=20,verbose_name='文件大小')   # KB/MB
    path = StringField(max_length=100,verbose_name='文件路径',null=False)
    download_count = IntField(default=0,verbose_name='下载次数')
    course = ReferenceField(Course)   # 资源对应的课程
    meta = {'collection': 'resource'}  # 数据库中的集合

    @staticmethod
    def save_resource(file, course, owner):
        """
        资源信息写入数据库
        :param file: 文件
        :param course: 课程
        :param owner:  上传者（教师）
        :return:
        """
        file_type = os.path.splitext(file.name)[1][1:]  # 获取文件后缀名 ppt/pdf
        # 文件大小单位转换
        if int(file.size / 1024) < 1024:
            file_size = str(round(file.size / 1024, 2)) + 'KB'
        else:
            file_size = str(round(file.size / 1024 / 1024, 2)) + 'MB'
        file_path = os.path.join(course.name, file.name)  # 文件的相对地址
        resource = Resource.objects.filter(path=file_path).first()
        if not resource:
            resource = Resource(name=file.name, type=file_type, size=file_size, owner=owner, path=file_path,
                                course=course)
            resource.save()
        else:
            # 更新资源数据库记录
            resource.download_count = 0
            resource.size = file_size
            resource.upload_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            resource.save()






