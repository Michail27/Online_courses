from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from clases.BaseExeption import ContentNotFound
from clases.courses.serializers import CourseSerializer
from clases.models import Course
from clases.permissions import IsTeacher, IsOwner


class CourseList(ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsTeacher]
    serializer_class = CourseSerializer

    def get_queryset(self):
        if self.request.user.role == 'teacher':
            return Course.objects.all()
        return Course.objects.filter(students=self.request.user.id)


class CourseDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def get_object(self):
        if Course.objects.get(pk=self.kwargs['course_id']).teacher_owner_id == self.request.user.id:
            return Course.objects.get(pk=self.kwargs['course_id'], teacher_owner=self.request.user)
        elif Course.objects.get(pk=self.kwargs['course_id']) in Course.objects.filter(students=self.request.user.id):
            return Course.objects.get(pk=self.kwargs['course_id'])

    def put(self, request, *args, **kwargs):
        course = Course.objects.get(pk=self.kwargs['course_id'], teacher_owner=self.request.user)
        serializer = CourseSerializer(data=request.data, instance=course)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
