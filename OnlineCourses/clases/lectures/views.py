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
        if self.request.user.id == Course.objects.get(pk=self.kwargs['course_id']).teacher_owner_id:
            return Lecture.objects.filter(course=self.kwargs['course_id'])
        elif Course.objects.get(pk=self.kwargs['course_id']) in Course.objects.filter(students=self.request.user.id):
            return Lecture.objects.filter(course=self.kwargs['course_id'])
        elif Course.objects.get(pk=self.kwargs['course_id']) in Course.objects.filter(teachers=self.request.user.id):
            return Lecture.objects.filter(lecture_owner=self.request.user)

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
        if self.request.user.id == Course.objects.get(pk=self.kwargs['course_id']).teacher_owner_id:
            return Lecture.objects.get(pk=self.kwargs['lecture_id'])
        elif Course.objects.get(pk=self.kwargs['course_id']) in Course.objects.filter(teachers=self.request.user.id):
            return Lecture.objects.get(pk=self.kwargs['lecture_id'])

    def put(self, request, *args, **kwargs):
        lecture = Lecture.objects.get(pk=self.kwargs['lecture_id'], lecture_owner=self.request.user)
        serializer = LectureSerializer(data=request.data, instance=lecture)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
