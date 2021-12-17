from django.urls import path

from clases.courses.views import CourseList, CourseDetail
from clases.lectures.views import LectureList, LectureDetail
from clases.views import Register, Login, logout_user

urlpatterns = [
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path("logout/", logout_user, name='logout'),
    path('courses/', CourseList.as_view(), name='courses_list'),
    path('courses/<int:course_id>/', CourseDetail.as_view(), name='course'),
    path('courses/<int:course_id>/lectures/', LectureList.as_view(), name='lectures_list'),
    path('courses/<int:course_id>/lectures/<int:lecture_id>/', LectureDetail.as_view(), name='lecture'),
]

