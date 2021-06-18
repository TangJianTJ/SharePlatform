#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File        :   urls.py    
@CopyRight   :   USTC SSE
@Modify Time :   2020/11/23 15:15
@Author      :   TJ
@Version     :   1.0
@Description :   course 路由
"""
from django.urls import path,re_path
from .views import *

urlpatterns = [
 path('course/',CourseView.as_view()),
 path('course/recommend',CourseRecommend.as_view()),
 path('course/upload',CourseUpload.as_view()),
 path('course/resource/',CourseResource.as_view()),
 re_path('course/(?P<pk>\\d+)',CourseObjectView.as_view({"get": "retrieve", "delete": "destroy", "put": "update"}))
]


