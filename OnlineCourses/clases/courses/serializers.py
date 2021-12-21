from rest_framework import serializers

from clases.models import Course, ProfileUser


class CourseSerializer(serializers.ModelSerializer):
    teachers = serializers.PrimaryKeyRelatedField(many=True,
                                                  queryset=ProfileUser.objects.filter(role='teacher'))
    students = serializers.PrimaryKeyRelatedField(many=True,
                                                  queryset=ProfileUser.objects.filter(role='student'))

    class Meta:
        model = Course
        fields = ['id', 'name', 'teacher_owner', 'teachers', 'students']

    def create(self, validated_data):
        request = self.context['request']
        validated_data['teacher_owner'] = request.user
        course = Course(name=validated_data.get('name'), teacher_owner=validated_data.get('teacher_owner'))
        course.save()
        course.teachers.set(validated_data.get('teachers', []))
        course.teachers.add(validated_data['teacher_owner'])
        course.students.set(validated_data.get('students', []))
        course.save()
        return course

    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.teachers.set(validated_data.get('teachers', instance.teachers.all()))
        instance.students.set(validated_data.get('students', instance.students.all()))
        instance.save()
        return instance
