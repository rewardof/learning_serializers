from django.db import models
from django import forms
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site



class Student(models.Model):
    choices = [
        ('T', 'technology'),
        ('M', 'medicine'),
        ('F', 'Finance'),
        ('P', 'politics'),
        ('s', 'social subjects'),
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    student_id = models.IntegerField(unique=True)
    entry_date = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(blank=True, max_length=254)
    faculty = models.ForeignKey('Faculty', on_delete=models.PROTECT)
    interests = models.TextField(max_length=200, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def full_name(self):
        return f'{self.first_name} {self.last_name}'



class StudentProfile(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', default='images/default.jpg')
    skills = models.ForeignKey('Skills', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.student.first_name} {self.student.last_name}'


class Mark(models.Model):
    student = models.ForeignKey(Student, related_name='student_marks', on_delete=models.CASCADE)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    mark = models.IntegerField()

    def __str__(self):
        return f'{self.student} - {self.subject} - {self.mark}'

    def get_absolute_url(self, *args, **kwargs):
        url = reverse(viewname='marks-detail', kwargs={'pk': self.pk})
        return url


class Faculty(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Faculties'


class Teacher(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    teacher_id = models.IntegerField()
    subject = models.ForeignKey('Subject', on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.first_name}--{self.last_name}'


class Subject(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class StudentSubjects(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'StudentSubjects'


class HighScore(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    player_name = models.CharField(max_length=10)
    score = models.IntegerField()


class Skills(models.Model):
    Skill = (
        ('It', 'IT'),
        ('copywriting', 'CW'),
        ('smm', 'SMM'),
    )
    category = models.CharField(max_length=255, choices=Skill)
    name = models.CharField(max_length=255)
