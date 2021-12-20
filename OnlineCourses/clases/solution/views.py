from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response

from clases.models import Course, Solution
from clases.permissions import IsStudent
from clases.solution.serializers import SolutionSerializer


class SolutionList(ListCreateAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, IsStudent]
    serializer_class = SolutionSerializer

    def get_queryset(self):
        if Course.objects.get(pk=self.kwargs['course_id']) in Course.objects.filter(teachers=self.request.user.id):
            return Solution.objects.filter(homework=self.kwargs['homework_id'],
                                           homework__lecture=self.kwargs['lecture_id'],
                                           homework__lecture__course=self.kwargs['course_id'])
        elif Course.objects.get(pk=self.kwargs['course_id']) in Course.objects.filter(students=self.request.user.id):
            return Solution.objects.filter(student=self.request.user,
                                           homework=self.kwargs['homework_id'],
                                           homework__lecture=self.kwargs['lecture_id'],
                                           homework__lecture__course=self.kwargs['course_id'])

    def post(self, request, *args, **kwargs):
        serializer = SolutionSerializer(data={'text': request.data['text'], 'student': request.user.id,
                                        'homework': kwargs['homework_id']})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SolutionDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsStudent]
    serializer_class = SolutionSerializer
    queryset = Course.objects.all()

    def get_object(self):
        if self.request.user.id == Solution.objects.filter(id=self.kwargs['solution_id']).get().student.id:
            return Solution.objects.get(id=self.kwargs['solution_id'])
        elif Course.objects.get(pk=self.kwargs['course_id']) in Course.objects.filter(teachers=self.request.user.id):
            return Solution.objects.get(id=self.kwargs['solution_id'])

#
    def put(self, request, *args, **kwargs):
        solution = Solution.objects.get(id=self.kwargs['solution_id'])
        serializer = SolutionSerializer(data=request.data, instance=solution)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

