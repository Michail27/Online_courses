from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response

from clases.mark.serializers import MarkSerializer
from clases.models import Course, Solution, Mark
from clases.permissions import IsStudent, IsTeacherCourse
from clases.solution.serializers import SolutionSerializer


class MarkList(ListCreateAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, IsTeacherCourse]
    serializer_class = MarkSerializer

    def get_queryset(self):
        if Course.objects.get(pk=self.kwargs['course_id']) in Course.objects.filter(teachers=self.request.user.id):
            return Mark.objects.filter(solution=self.kwargs['solution_id'],
                                       solution__homework=self.kwargs['homework_id'],
                                       solution__homework__lecture=self.kwargs['lecture_id'],
                                       solution__homework__lecture__course=self.kwargs['course_id'])
        elif self.request.user.id == Solution.objects.get(pk=self.kwargs['solution_id']).student.id:
            return Mark.objects.filter(solution=self.kwargs['solution_id'],
                                       solution__homework=self.kwargs['homework_id'],
                                       solution__homework__lecture=self.kwargs['lecture_id'],
                                       solution__homework__lecture__course=self.kwargs['course_id'])

    def post(self, request, *args, **kwargs):
        serializer = MarkSerializer(data={'mark': request.data['mark'], 'teacher': request.user.id,
                                          'solution': kwargs['solution_id']})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
