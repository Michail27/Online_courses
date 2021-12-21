from django.urls import path

from clases.comment.views import CommentList
from clases.courses.views import CourseList, CourseDetail
from clases.homework.views import HomeworkList, HomeworkDetail
from clases.lectures.views import LectureList, LectureDetail
from clases.mark.views import MarkList
from clases.solution.views import SolutionList, SolutionDetail
from clases.views import Register, Login, logout_user

urlpatterns = [
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path("logout/", logout_user, name='logout'),

    path('courses/', CourseList.as_view(), name='courses_list'),
    path('courses/<int:course_id>/', CourseDetail.as_view(), name='course'),

    path('courses/<int:course_id>/lectures/', LectureList.as_view(), name='lectures_list'),
    path('courses/<int:course_id>/lectures/<int:lecture_id>/', LectureDetail.as_view(), name='lecture'),

    path('courses/<int:course_id>/lectures/<int:lecture_id>/homework/', HomeworkList.as_view()),
    path('courses/<int:course_id>/lectures/<int:lecture_id>/homework/<int:homework_id>/', HomeworkDetail.as_view()),

    path('courses/<int:course_id>/lectures/<int:lecture_id>/homework/<int:homework_id>/solution/',
         SolutionList.as_view()),
    path('courses/<int:course_id>/lectures/<int:lecture_id>/homework/<int:homework_id>/solution/<int:solution_id>/',
         SolutionDetail.as_view()),

    path('courses/<int:course_id>/lectures/<int:lecture_id>/homework/<int:homework_id>/solution/<int:solution_id>/mark',
         MarkList.as_view()),

    path('courses/<int:course_id>/lectures/<int:lecture_id>/homework/<int:homework_id>/solution/<int:solution_id>/'
         'mark/<int:mark_id>/comments/', CommentList.as_view())
]
