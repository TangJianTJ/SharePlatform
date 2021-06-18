from django.urls import path
from .views import *

urlpatterns = [
    path('user/info/', UserView.as_view()),
    path('user/course/', UserCoursers.as_view()),
    path('course/add/',AddCourse.as_view())
]