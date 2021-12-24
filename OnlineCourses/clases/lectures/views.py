from django.http import Http404
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response

from clases.lectures.serializers import LectureSerializer
from clases.models import Course, Lecture
from clases.permissions import IsTeacherCourse


class LectureList(ListCreateAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, IsTeacherCourse]
    serializer_class = LectureSerializer
    queryset = Lecture.objects.all()

    def get_queryset(self):
        if Course.objects.get(pk=self.kwargs['course_id']) in Course.objects.filter(teachers=self.request.user.id):
            return Lecture.objects.filter(course=self.kwargs['course_id'])
        elif Course.objects.get(pk=self.kwargs['course_id']) in Course.objects.filter(students=self.request.user.id):
            return Lecture.objects.filter(course=self.kwargs['course_id'])
        else:
            raise Http404

    def post(self, request, *args, **kwargs):
        serializer = LectureSerializer(data={'topic_lecture': request.data['topic_lecture'],
                                             'presentation': request.data['presentation'],
                                             'lecture_owner': request.user.id,
                                             'course': kwargs['course_id']})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LectureDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsTeacherCourse]
    serializer_class = LectureSerializer
    queryset = Course.objects.all()

    def get_object(self):
        if Course.objects.get(pk=self.kwargs['course_id']) in Course.objects.filter(teachers=self.request.user.id):
            return Lecture.objects.get(pk=self.kwargs['lecture_id'])
        elif Course.objects.get(pk=self.kwargs['course_id']) in Course.objects.filter(students=self.request.user.id):
            return Lecture.objects.get(pk=self.kwargs['lecture_id'])
        else:
            raise Http404

    def put(self, request, *args, **kwargs):
        lecture = Lecture.objects.get(pk=self.kwargs['lecture_id'])
        serializer = LectureSerializer(data=request.data, instance=lecture)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
