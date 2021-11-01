from django.contrib import admin
from .models import Student, Subject, Mark, Faculty, Teacher, StudentSubjects, StudentProfile, HighScore, Skills

admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(Mark)
admin.site.register(Faculty)
admin.site.register(Teacher)
admin.site.register(StudentSubjects)
admin.site.register(StudentProfile)
admin.site.register(HighScore)
admin.site.register(Skills)