import os
import logging
import mimetypes
from django.shortcuts import render,HttpResponse
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from django.http import StreamingHttpResponse,FileResponse
from rest_framework.response import Response
from django.utils.http import urlquote
from login.login_token import resolve_token
from course.models import Course
from .models import Resource
from user.models import Teacher
from pathlib import Path
from django.utils._os import safe_join
from SharePlatform.settings import MEDIA_ROOT
# Create your views here.


def hello(request):
    return HttpResponse('Hello World!')


class FileUploadView(APIView):
    permission_classes = []
    path = os.path.join(MEDIA_ROOT,'files')
    logger = logging.getLogger('resource.views')

    def get(self,request):
        return render(self.request,'index.html')

    @resolve_token
    def post(self, request, args):
        """
        上传文件
        :param request: 上传文件列表
        :param args:
        :return:
        """
        if args.get('role') == 'student':
            return Response({'code': 401, 'msg': 'you have no authority'}, status=200)
        files = request.FILES.getlist('file', None)  # 获取上传文件列表
        if not files:
            return Response({'code': 400, 'msg': 'no files upload'},status=200)
        course_id = request.query_params.get('id')
        file_owner = Teacher.objects.get(uid = args.get('uid'))
        print(course_id)
        course = Course.objects.get(id=course_id)
        self.path = os.path.join(self.path,course.name)  # 以课程名为文件夹名
        if not os.path.exists(self.path):
            self.logger.info('folder is not exist')
            os.makedirs(self.path)  # 创建存储文件的文件夹
        # 文件写入磁盘
        for file in files:
            self.logger.info('上传'+file.name)
            destination = open(os.path.join(self.path, file.name), 'wb')
            print('文件名：'+file.name+'\n'+'文件大小：'+str(file.size/1024)+'KB')
            for chunk in file.chunks():
                destination.write(chunk)
            destination.close()
            # 文件信息写入数据库
            Resource.save_resource(file,course,file_owner)
        return Response({'code': 201,'msg': 'upload success'},status=201)

    @csrf_exempt  # 关闭csrf防护
    def dispatch(self, request, *args, **kwargs):
        return super(FileUploadView, self).dispatch(request,*args, **kwargs)


class FileDownloadView(APIView):
    permission_classes = []
    path = os.path.join(MEDIA_ROOT, 'files')
    logger = logging.getLogger('resource.views')

    def get(self,request, resource_id):
        """
        直接下载
        :param request:
        :param resource_id: 资源id
        :return: file
        """
        resource = Resource.objects.get(pk=resource_id)
        self.path = os.path.join(self.path,resource.path)
        file_name = resource.name

        if not os.path.exists(self.path):
            return Response({'code': 404,'msg':'资源找不到'},status = 404)
        self.logger.info('下载' + file_name)
        resource.download_count=resource.download_count+1
        resource.save()
        response = StreamingHttpResponse(file_iterator(self.path))
        response['Content-Type'] = 'application/octet-stream'  # 文件流格式
        response['Content-Disposition'] = 'attachment;filename="%s"' % (urlquote(file_name))  # 下载显示文件名中文必须加上urlquote进行编码
        return response

    def post(self,request):
        """
        文件下载
        :param request: recourseId
        :return:msg
        """
        file_path = request.data.get('filePath','《算法图解》.pdf')
        file_name = request.data.get('fileName','《算法图解》.pdf')
        if not file_path:
            return HttpResponse('no filePath')
        #ab_file_path = os.path.join(self.path,file_path)
        ab_file_path = Path(safe_join(self.path, file_path))
        response = FileResponse(ab_file_path.open('rb'), content_type='application/pdf')
        # response = StreamingHttpResponse(file_iterator(ab_file_path))
       # response['Content-Type'] = 'application/octet-stream'     # 文件流格式
        #response['Content-Type'] = 'application/pdf'  # pdf格式
        response['Content-Disposition'] = 'attachment;filename="%s"' % (urlquote(file_name)) # 下载显示文件名中文必须加上urlquote进行编码
        return response


def preview(request):
    """
    资源预览
    :param request:
    :return:
    """
    if request.method == 'POST':
        return HttpResponse('hello word')
    path = 'E:\\receive\\resources'
    file_path = 'django简介.pptx'
    file_name = '《算法图解》.pdf'
    if not file_path:
        return HttpResponse('no filePath')
    # ab_file_path = os.path.join(self.path,file_path)
    ab_file_path = Path(safe_join(path, file_path))
    content_type, encoding = mimetypes.guess_type(str(ab_file_path))
    content_type = content_type or 'application/octet-stream'
    response = FileResponse(ab_file_path.open('rb'), content_type=content_type)
    return response


def file_iterator(file_path, chunk_size=512):
    """
    生成器函数，分块读取磁盘文件
    :param file_path: 文件绝对路径
    :param chunk_size: 块大小
    :return:
    """
    with open(file_path, 'rb') as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break


