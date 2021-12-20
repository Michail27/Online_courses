from rest_framework import serializers

from clases.models import Homework


class HomeworkSerializer(serializers.ModelSerializer):

    class Meta:
        model = Homework
        fields = '__all__'

