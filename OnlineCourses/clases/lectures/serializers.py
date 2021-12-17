from rest_framework import serializers

from clases.models import Lecture


class LectureSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lecture
        fields = '__all__'

