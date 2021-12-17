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
    # queryset = Lecture.objects.all()

    def get_queryset(self):
        if self.request.user.id == Course.objects.get(pk=self.kwargs['course_id']).teacher_owner_id:
            return Lecture.objects.filter(course=self.kwargs['course_id'], lecture_owner=self.request.user)
        return Lecture.objects.filter(course=self.kwargs['course_id'])

    def post(self, request, *args, **kwargs):
        self.create(request, *args, **kwargs)
        return Response('Lecture create', status=status.HTTP_201_CREATED)


class LectureDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsTeacherCourse]
    serializer_class = LectureSerializer
    queryset = Course.objects.all()

    def get_object(self):
        if self.request.user.id == Course.objects.get(pk=self.kwargs['course_id']).teacher_owner_id:
            return Lecture.objects.get(pk=self.kwargs['lecture_id'])
        return Lecture.objects.get(pk=self.kwargs['lecture_id'])

    def put(self, request, *args, **kwargs):
        lecture = Lecture.objects.get(pk=self.kwargs['lecture_id'], lecture_owner=self.request.user)
        serializer = LectureSerializer(data=request.data, instance=lecture)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
