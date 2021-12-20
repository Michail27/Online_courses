from rest_framework import serializers

from clases.models import Lecture


class LectureSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lecture
        fields = '__all__'

    def create(self, validated_data, **kwargs):
        lecture = Lecture(**validated_data)
        lecture.save()
        return lecture

    def update(self, instance, validated_data):
        instance.topic_lecture = validated_data['topic_lecture']
        instance.presentation = validated_data['presentation']
        instance.save()
        return instance

