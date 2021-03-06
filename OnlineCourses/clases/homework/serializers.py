from rest_framework import serializers

from clases.models import Homework


class HomeworkSerializer(serializers.ModelSerializer):

    class Meta:
        model = Homework
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.task = validated_data['task']
        instance.save()
        return instance

