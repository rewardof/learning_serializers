# Generated by Django 3.2.7 on 2021-12-17 14:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0006_auto_20211217_1827'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeacherLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.IntegerField(choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')])),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='level', to='student.teacher')),
            ],
        ),
        migrations.CreateModel(
            name='StudentLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.IntegerField(choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')])),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='level', to='student.student')),
            ],
        ),
    ]
