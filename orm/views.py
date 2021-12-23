from django.db.models import OuterRef, Subquery, Count, F
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response

from .serializers import HeroSerializer, CategorySerializer, CategoryWithCountSerializer
from .models import Hero, Category
from rest_framework.generics import ListCreateAPIView


class HeroListView(ListCreateAPIView):
    queryset = Hero.objects.all()
    serializer_class = HeroSerializer

    def get(self, *args, **kwargs):
        number_of_categories = 2
        hero_qs = Hero.objects.filter(category=OuterRef("pk")).order_by("-benevolence_factor")
        category = Category.objects.all().annotate(most_benevolent_hero=Subquery(hero_qs.values('name')[:1]))
        categories = CategorySerializer(category, many=True).data

        heros = Hero.objects.values('category').annotate(count_category=Count('category'))
        heros = CategoryWithCountSerializer(heros, many=True).data

        category = Category.objects.filter(hero_count__gt=number_of_categories)
        print(category)

        payload = {
            'categories': categories,
            'heros': heros,
        }
        return Response(payload, status=status.HTTP_200_OK)
