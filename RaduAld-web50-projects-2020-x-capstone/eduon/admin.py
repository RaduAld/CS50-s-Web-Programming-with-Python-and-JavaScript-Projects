from django.contrib import admin
from .models import User, Subject, Grade, Announcement, Homework, Class_school

admin.site.register(User)
admin.site.register(Subject)
admin.site.register(Grade)
admin.site.register(Announcement)
admin.site.register(Homework)
admin.site.register(Class_school)