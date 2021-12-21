from rest_framework import serializers

from clases.models import Lecture


class LectureSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lecture
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.topic_lecture = validated_data['topic_lecture']
        instance.presentation = validated_data['presentation']
        instance.save()
        return instance

