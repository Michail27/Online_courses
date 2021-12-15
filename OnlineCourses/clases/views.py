from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from clases.models import ProfileUser
from clases.serializers import RegisterSerializers


class Register(GenericAPIView):
    serializer_class = RegisterSerializers

    def post(self, request):
        if not ProfileUser.objects.filter(username=request.data['username']):
            serializer = self.get_serializer(data=request.data)
            if request.data.get('role'):
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response({"Your Userprofile is registered"}, status=status.HTTP_200_OK)
            else:
                return Response({'You mast chaise role'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"this Userprofile already exist"}, status=status.HTTP_403_FORBIDDEN)
