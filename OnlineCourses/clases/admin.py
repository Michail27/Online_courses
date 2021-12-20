from django.contrib import admin

from clases.models import ProfileUser, Course, Lecture, Homework, Solution

admin.site.register(ProfileUser)
admin.site.register(Course)
admin.site.register(Lecture)
admin.site.register(Homework)
admin.site.register(Solution)
