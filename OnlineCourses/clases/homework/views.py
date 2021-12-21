from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response

from clases.BaseExeption import ContentNotFound
from clases.homework.serializers import HomeworkSerializer

from clases.models import Course, Homework
from clases.permissions import IsTeacherCourse


class HomeworkList(ListCreateAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, IsTeacherCourse]
    serializer_class = HomeworkSerializer

    def get_queryset(self):
        if Course.objects.get(pk=self.kwargs['course_id']) in Course.objects.filter(teachers=self.request.user.id):
            return Homework.objects.filter(lecture=self.kwargs['lecture_id'])
        elif Course.objects.get(pk=self.kwargs['course_id']) in Course.objects.filter(students=self.request.user.id):
            return Homework.objects.filter(lecture=self.kwargs['lecture_id'])
        else:
            raise ContentNotFound({"error": ["You don't have access to these tasks"]})

    def post(self, request, *args, **kwargs):
        serializer = HomeworkSerializer(data={'task': request.data['task'],
                                              'tasks_owner': request.user.id,
                                              'lecture': kwargs['lecture_id']})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HomeworkDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsTeacherCourse]
    serializer_class = HomeworkSerializer
    queryset = Course.objects.all()

    def get_object(self):
        if Course.objects.get(pk=self.kwargs['course_id']) in Course.objects.filter(teachers=self.request.user.id):
            return Homework.objects.get(pk=self.kwargs['homework_id'])
        elif Course.objects.get(pk=self.kwargs['course_id']) in Course.objects.filter(students=self.request.user.id):
            return Homework.objects.get(pk=self.kwargs['homework_id'])
        else:
            raise ContentNotFound({"error": ["You don't have access to this task"]})

    def put(self, request, *args, **kwargs):
        task = Homework.objects.get(pk=self.kwargs['homework_id'])
        serializer = HomeworkSerializer(data=request.data, instance=task)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

