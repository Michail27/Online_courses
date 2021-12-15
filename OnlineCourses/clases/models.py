from django.contrib.auth.models import AbstractUser
from django.db import models


class ProfileUser(AbstractUser):
    role = models.CharField(max_length=10, choices=[('student', 'student'), ('teacher', 'teacher')],
                            null=True, blank=True, )

