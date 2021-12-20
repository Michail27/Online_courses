from rest_framework import permissions
from rest_framework.permissions import BasePermission

from clases.models import Course


class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role == 'teacher'


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        course = Course.objects.get(id=view.kwargs['course_id'])
        return request.user in course.students.all()


class IsOwner(BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        course = Course.objects.get(id=view.kwargs['course_id']).teacher_owner_id
        return request.user.id == course


class IsTeacherCourse(BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        course = Course.objects.get(id=view.kwargs['course_id'])
        return request.user in course.teachers.all()
