import logging

from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import StudentSerializers,TeacherSerializers
from login.login_token import *
from .models import *
from course.models import Course
from course.serializers import CourseSerializers
from SharePlatform.settings import BASE_URL
# Create your views here.

logger = logging.getLogger('user.views')


class UserView(APIView):
    # 修改用户信息
    @resolve_token
    def get(self,request,args):
        if args.get('role') == 'student':
            student = Student.objects.filter(uid=args.get('uid')).first()
            student.password = ''
            serializer = StudentSerializers(student)
        else:
            teacher = Teacher.objects.filter(uid=args.get('uid')).first()
            teacher.password = ''
            serializer = TeacherSerializers(teacher)
        return Response({'code':200,'msg':'获取用户信息成功！','data':serializer.data},status=200)

    @resolve_token
    def put(self,request,args):
        data ={'code': 400}
        if args.get('role') == 'student':
            student = Student.objects.filter(uid=args.get('uid')).first()
            serializers = StudentSerializers(student,data=request.data)
        else:
            teacher = Teacher.objects.filter(uid=args.get('uid')).first()
            serializers = TeacherSerializers(teacher,data=request.data)
        try:
            if serializers.is_valid(raise_exception=True):
                user = serializers.save()
                data['code'] = '200'
                data['msg'] = '修改成功'
                data['data'] = serializers.data
                logger.info('修改'+user.username+'信息成功！')
                return Response(data,status=200)
        except Exception as e:
            data['msg'] = '修改失败'
            logger.info('修改' + serializers.data.get('username') + '信息成功！')
            print(e)
        return Response(data,status=400)


class UserCoursers(APIView):
    baseUrl = BASE_URL
    course_list = []

    @resolve_token
    def get(self,request, args):
        """
        根据教师的id获取教师的课程或根据学生id获取所添加课程
        :param request:
        :param args:
        :return: list[courses]
        """
        if args.get('role') == 'teacher':
            uid = args.get('uid')
            self.course_list = Course.objects.filter(owner_id=uid)
        elif args.get('role') == 'student':
            uid = args.get('uid')
            self.course_list = Student.objects.get(uid=uid).add_course
        else:
            return Response({'code':403,'msg':'未授权的请求'},status=403)
        for course in self.course_list:
            course.image=self.baseUrl+course.image
            serializer = CourseSerializers(self.course_list,many=True)
            logger.info('获取用户'+args.get('username')+'课程列表成功！')
            return Response({'code':200,'msg':'获取课程列表成功！','data':serializer.data},status=200)


class AddCourse(APIView):
    @resolve_token
    def get(self,request,args):
        """
        获取学生已添加课程列表，判断是否包含该课程(0/1)
        :param request: 包含课程id
        :param args:
        :return:
        """
        is_add = 0
        if args.get('role') == 'student':
            uid = args.get('uid')
            course_id = request.query_params.get('id')
            course_list = Student.objects.get(uid=uid).add_course
            course = Course.objects.get(id=course_id)
            if course in course_list:
                is_add = 1
        logger.info('is_add'+str(is_add))
        return Response({'code':'200','msg':'请求成功！','is_add':is_add},status=200)

    @resolve_token
    def post(self,request,args):
        """
        添加我的课程
        :param request:
        :param args:
        :return:
        """
        data = {'code':400}
        if args.get('role') == 'student':
            uid = args.get('uid')
            course_id = request.data.get('course_id',None)
            student = Student.objects.get(uid=uid)
            if course_id:
                course = Course.objects.get(id=course_id)
                if course not in student.add_course:
                    student.add_course.append(course)
                    course.add_count=course.add_count+1
                    student.save()
                    course.save()
                    logger.info('用户' + args.get('username') + '成功添加课程' + course.name)
                    data['code'] = 200
                    data['msg'] = '添加成功！'
                else:
                    data['msg'] = '已添加该课程！'
                return Response({'data':data},status=200)
            else:
                data['code'] = 404
                data['msg'] = '该课程不存在！'
                return Response({'data':data},status=404)
        else:
            data['msg'] = '请使用学生账号登录选课！'
            return Response({'data':data},status=400)











