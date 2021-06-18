#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File        :   urls.py    
@CopyRight   :   USTC SSE
@Modify Time :   2020/11/21 15:13
@Author      :   TJ
@Version     :   1.0
@Description :   None
"""
from django.urls import path,re_path
from .views import *

urlpatterns = [
    path('course/uploadFiles/',FileUploadView.as_view()),
    re_path('course/resource/download/(?P<resource_id>\\d+)',FileDownloadView.as_view()),
    path('downloadFiles',FileDownloadView.as_view()),
    path('preview/',preview)
]
    

