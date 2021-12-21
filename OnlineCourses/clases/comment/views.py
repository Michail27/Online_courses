from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response

from clases.BaseExeption import ContentNotFound
from clases.comment.serializers import CommentSerializer

from clases.models import Course, Comment, Solution


class CommentList(ListCreateAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def get_queryset(self):
        if Course.objects.get(pk=self.kwargs['course_id']) in Course.objects.filter(teachers=self.request.user.id):
            return Comment.objects.filter(mark=self.kwargs['mark_id'])
        elif self.request.user.id == Solution.objects.filter(pk=self.kwargs['solution_id']).get().student.id:
            return Comment.objects.filter(mark=self.kwargs['mark_id'])
        else:
            raise ContentNotFound({"error": ["You don't have access to these Comments"]})

    def post(self, request, *args, **kwargs):
        serializer = CommentSerializer(data={'comment': request.data['comment'],
                                             'user': request.user.id,
                                             'mark': kwargs['mark_id']})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
