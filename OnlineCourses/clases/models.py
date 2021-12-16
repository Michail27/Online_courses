from django.contrib.auth.models import AbstractUser
from django.db import models


class ProfileUser(AbstractUser):
    role = models.CharField(max_length=10, choices=[('student', 'student'), ('teacher', 'teacher')],
                            null=True, blank=True, )


class Course(models.Model):
    name = models.CharField(max_length=200)
    teacher_owner = models.ForeignKey(ProfileUser, on_delete=models.CASCADE)

    students = models.ManyToManyField(ProfileUser, related_name='students_course')
    teachers = models.ManyToManyField(ProfileUser, related_name='teachers_course')

    def __str__(self):
        return f'{self.name}'



