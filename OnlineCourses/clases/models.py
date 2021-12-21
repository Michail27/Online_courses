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


class Lecture(models.Model):
    topic_lecture = models.CharField(max_length=300, blank=False)
    presentation = models.FileField(upload_to='uploads/')
    lecture_owner = models.ForeignKey(ProfileUser, on_delete=models.CASCADE,  related_name='lectures')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lectures')

    def __str__(self):
        return self.topic_lecture


class Homework(models.Model):
    task = models.TextField(blank=False)
    tasks_owner = models.ForeignKey(ProfileUser, on_delete=models.CASCADE,  related_name='tasks')
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, blank=False, related_name='tasks')

    def __str__(self):
        return self.task


class Solution(models.Model):
    text = models.TextField()
    student = models.ForeignKey(ProfileUser, on_delete=models.CASCADE, related_name='solution')
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, related_name='solution')

    def __str__(self):
        return self.text


class Mark(models.Model):
    mark = models.IntegerField()
    teacher = models.ForeignKey(ProfileUser, on_delete=models.CASCADE, related_name='mark')
    solution = models.ForeignKey(Solution, on_delete=models.CASCADE, related_name='mark')

    def __str__(self):
        return self.mark


class Comment(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(ProfileUser, on_delete=models.CASCADE, related_name='comment')
    mark = models.ForeignKey(Mark, on_delete=models.CASCADE, related_name='comment')

    def __str__(self):
        return self.comment
