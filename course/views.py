import os
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CourseSerializers
from login.login_token import *
from .models import Course
from rest_framework.viewsets import ModelViewSet
from SharePlatform.settings import MEDIA_ROOT
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
""""
创建课程的视图函数
"""


class CourseView(APIView):

    path = os.path.join(MEDIA_ROOT,os.path.join('images','course'))
    @resolve_token
    def post(self,request,args):
        data = {'code': 401}
        if args.get('role') == 'student':
            data['msg'] = 'you have no authority'
            return Response(data,status=401)
        course = request.data.copy()           # query_dict不可变，从此需要copy
        course['owner_id'] = args.get('uid')  # 创建人的uid
        course['owner_name'] = args.get('name')  # 创建人的name
        #  图片写入磁盘
        image = request.FILES.get('image',None)
        if image is not None:
            destination = open(os.path.join(self.path, image.name), 'wb')
            print('文件名：' + image.name + '\n' + '文件大小：' + str(image.size / 1024) + 'KB')
            for chunk in image.chunks():
                destination.write(chunk)
            destination.close()
            course['image'] = 'images/course'+'/'+image.name
        serializer = CourseSerializers(data=course)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                data['code'] = 201
                data['msg'] = 'created successful'
                return Response(data,status=201)
            else:
                data['code'] = 401
                data['msg'] = 'created failed '
                return Response(data,status=401)
        except Exception as e:
            print(e)
        return Response(data,status=401)

    def get(self,request):
        """
        获取所有课程列表
        :param request:
        :return:
        """
        courses = Course.objects.all()
        serializers = CourseSerializers(courses,many=True)
        return Response({'code':200,'data':serializers.data,'msg':'获取课程列表成功'},status=200)



class CourseObjectView(ModelViewSet):
    permission_classes = []
    queryset = Course.objects.all()
    serializer_class = CourseSerializers

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({'code': 200, 'msg': '获取课程信息成功！', 'data': serializer.data}, status=200)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response({'code': 200, 'msg': '修改课程信息成功！', 'data': serializer.data}, status=200)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'code': 200, 'msg': '删除课程成功！'},status=204)



















