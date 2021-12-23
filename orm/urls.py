from django.urls import path, include
from orm import views


urlpatterns = [
    path('hero_and_category/', views.HeroListView.as_view(), name='hero_and_category'),
]