# Generated by Django 3.2.7 on 2021-12-21 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orm', '0002_category_hero_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
    ]
