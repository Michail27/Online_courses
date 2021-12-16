from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, DestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from clases.courses.serializers import CourseSerializer
from clases.models import Course
from clases.permissions import IsTeacher


class CourseList(ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsTeacher]
    serializer_class = CourseSerializer

    def get_queryset(self):
        if self.request.user.role == 'teacher':
            return Course.objects.filter(teacher_owner=self.request.user.id)
        return Course.objects.all()

class CourseDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsTeacher]
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def get_object(self):
        if self.request.user.role == 'teacher':
            return Course.objects.get(pk=self.kwargs['pk'], teacher_owner=self.request.user)
        return Course.objects.get(pk=self.kwargs['pk'])

    def put(self, request, *args, **kwargs):
        course = Course.objects.get(pk=self.kwargs['pk'], teacher_owner=self.request.user)
        serializer = CourseSerializer(data=request.data, instance=course)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
