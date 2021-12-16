from django.urls import path

from clases.courses.views import CourseList, CourseDetail
from clases.views import Register, Login, logout_user

urlpatterns = [
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path("logout/", logout_user, name='logout'),
    path('courses/', CourseList.as_view(), name='courses_list'),
    path('courses/<int:pk>/', CourseDetail.as_view(), name='course'),
]
