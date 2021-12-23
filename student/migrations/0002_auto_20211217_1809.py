# Generated by Django 3.2.7 on 2021-12-17 13:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='faculty',
            name='slug',
            field=models.SlugField(default='slug', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='mark',
            name='mark',
            field=models.IntegerField(choices=[(1, 'One'), (2, 'Two'), (3, 'Three'), (4, 'Four'), (5, 'Five')]),
        ),
        migrations.AlterField(
            model_name='student',
            name='faculty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.faculty'),
        ),
    ]
