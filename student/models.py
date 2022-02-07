from django.db import models
from django import forms
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.text import slugify


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
    faculty = models.ForeignKey('Faculty', on_delete=models.CASCADE, related_name='students', blank=True, null=True)
    interests = models.TextField(max_length=200, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class StudentProfile(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(upload_to='images/', default='images/default.jpg')
    skills = models.ForeignKey('Skills', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.student.first_name} {self.student.last_name}'


class Mark(models.Model):
    choices = [
        (1, 'One'),
        (2, 'Two'),
        (3, 'Three'),
        (4, 'Four'),
        (5, 'Five'),
    ]
    student = models.ForeignKey(Student, related_name='student_marks', on_delete=models.CASCADE)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, related_name='marks')
    mark = models.IntegerField(choices=choices)

    def __str__(self):
        return f'{self.student} - {self.subject} - {self.mark}'

    def get_absolute_url(self, *args, **kwargs):
        url = reverse(viewname='marks-detail', kwargs={'pk': self.pk})
        return url


class Faculty(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Faculties'
        
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.slug:
            slug = slugify(self.name)
        else:
            slug = self.slug
        self.slug = slug
        self.save()
        return super(Faculty, self).save()


class Teacher(models.Model):
    LEVEL = (
        (1, 'Assistent'),
        (2, 'Senior Teacher'),
        (3, 'PhD'),
        (4, 'Professor')
    )
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    scientific_level = models.IntegerField(choices=LEVEL)
    teacher_id = models.IntegerField()
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, related_name='teachers')

    def __str__(self):
        return f'{self.first_name} {self.last_name} --- {self.subject}'


class Subject(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class StudentSubjects(models.Model):
    choices = [
        (1, 'One'),
        (2, 'Two'),
    ]
    term = models.IntegerField(choices=choices)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='subjects')
    teacher = models.ForeignKey(Teacher, related_name='students', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.student.first_name} {self.student.last_name} subjects'

    class Meta:
        verbose_name_plural = 'Student Subjects'


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


class StudentLevel(models.Model):
    level = (
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High'),
    )
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='level')
    level = models.IntegerField(choices=level)

    def __str__(self):
        return f'{self.student.first_name} {self.student.last_name} level {self.level}'


class TeacherLevel(models.Model):
    level = (
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High'),
    )
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='level')
    level = models.IntegerField(choices=level)

    def __str__(self):
        return f'{self.teacher.first_name} {self.teacher.last_name} level {self.level}'
