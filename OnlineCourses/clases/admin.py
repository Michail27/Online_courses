from django.contrib import admin

from clases.models import ProfileUser, Course, Lecture

admin.site.register(ProfileUser)
admin.site.register(Course)
admin.site.register(Lecture)
