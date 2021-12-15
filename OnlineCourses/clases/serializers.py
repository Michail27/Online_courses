from rest_framework.serializers import ModelSerializer

from clases.models import ProfileUser


class RegisterSerializers(ModelSerializer):
    class Meta:
        model = ProfileUser
        fields = ('id', 'username', 'password', 'email', 'role')
        extra_kwargs = {'role': {'required': True}, }

    def create(self, validated_date):
        user = ProfileUser.objects.create_user(username=validated_date['username'],
                                               email=validated_date['email'],
                                               password=validated_date['password'],
                                               role=validated_date['role'],)
        return user
