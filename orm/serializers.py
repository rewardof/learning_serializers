from rest_framework import serializers
from .models import Hero, Category


class HeroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hero
        fields = ('id', 'name', 'category', 'benevolence_factor')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class CategoryWithCountSerializer(serializers.Serializer):
    count_category = serializers.IntegerField()
    category = serializers.IntegerField()

