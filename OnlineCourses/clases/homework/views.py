from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response

from clases.homework.serializers import HomeworkSerializer
from clases.lectures.serializers import LectureSerializer
from clases.models import Course, Lecture, Homework
from clases.permissions import IsTeacherCourse


class HomeworkList(ListCreateAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, IsTeacherCourse]
    serializer_class = HomeworkSerializer

    def get_queryset(self):
        if self.request.user.id == Course.objects.get(pk=self.kwargs['course_id']).teacher_owner_id:
            return Homework.objects.filter(lecture=self.kwargs['lecture_id'])
        elif Course.objects.get(pk=self.kwargs['course_id']) in Course.objects.filter(students=self.request.user.id):
            return Homework.objects.filter(lecture=self.kwargs['lecture_id'])
        elif Course.objects.get(pk=self.kwargs['course_id']) in Course.objects.filter(teachers=self.request.user.id):
            return Homework.objects.filter(lecture=self.kwargs['lecture_id'])

    def post(self, request, *args, **kwargs):
        self.create(request, *args, **kwargs)
        return Response('Task add', status=status.HTTP_201_CREATED)


class HomeworkDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsTeacherCourse]
    serializer_class = HomeworkSerializer
    queryset = Course.objects.all()

    def get_object(self):
        if self.request.user.id == Course.objects.get(pk=self.kwargs['course_id']).teacher_owner_id:
            return Homework.objects.get(pk=self.kwargs['homework_id'])
        elif Course.objects.get(pk=self.kwargs['course_id']) in Course.objects.filter(teachers=self.request.user.id):
            return Homework.objects.get(pk=self.kwargs['homework_id'])

    def put(self, request, *args, **kwargs):
        task = Homework.objects.get(pk=self.kwargs['homework_id'])
        serializer = HomeworkSerializer(data=request.data, instance=task)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

