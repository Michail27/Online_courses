from django.contrib import auth
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from clases.models import ProfileUser
from clases.serializers import RegisterSerializers, LoginSerializers


class Register(GenericAPIView):
    serializer_class = RegisterSerializers

    def post(self, request):
        if not ProfileUser.objects.filter(username=request.data['username']):
            serializer = self.get_serializer(data=request.data)
            if request.data.get('role'):
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response({"Your Userprofile is registered"}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)
        return Response({"this Userprofile already exist"}, status=status.HTTP_403_FORBIDDEN)


class Login(GenericAPIView):
    serializer_class = LoginSerializers

    def post(self, request):
        user = auth.authenticate(request,
                                 username=request.data['username'],
                                 password=request.data['password']
                                 )
        if user is not None:
            login(request, user)
            return Response({}, status=status.HTTP_200_OK)
        return Response('This user is not exist', status=status.HTTP_401_UNAUTHORIZED)


def logout_user(request):
    logout(request)
    return redirect('http://127.0.0.1:8000/clases/login/')
