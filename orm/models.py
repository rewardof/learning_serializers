from django.db import models
from django.db.models import F
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Category(models.Model):
    name = models.CharField(max_length=100)
    hero_count = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Hero(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    benevolence_factor = models.PositiveSmallIntegerField(
        help_text="How benevolent this hero is?",
        default=50
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            Category.objects.filter(pk=self.category_id).update(hero_count=F('hero_count') + 1)
        super().save(*args, **kwargs)


# @receiver(pre_save, sender=Hero, dispatch_uid="update_hero_count")
# def update_hero_count(sender, **kwargs):
#     hero = kwargs['instance']
#     Category.objects.filter(pk=hero.category_id).update(hero_count=F('hero_count') + 1)


class TestModel(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    @classmethod
    def truncate(cls):
        with connection.cursor() as cursor:
            cursor.execute('TRUNCATE TABLE "{0}" CASCADE'.format(cls._meta.db_table))
