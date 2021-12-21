from rest_framework import serializers

from clases.models import Mark


class MarkSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mark
        fields = '__all__'

    def create(self, validated_data):
        mark, created = Mark.objects.update_or_create(defaults={'mark': validated_data['mark']},
                                                      teacher=validated_data['teacher'],
                                                      solution=validated_data['solution'])
        return mark
