from rest_framework import serializers

from clases.models import Solution


class SolutionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Solution
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.text = validated_data['text']
        instance.save()
        return instance
