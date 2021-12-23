from django.contrib import admin
from django.urls import path, include

from book import views

urlpatterns = [
    path('books_json_create/', views.BookJsonCreateView.as_view()),
    path('authors_json_create/', views.AuthorJsonCreateView.as_view()),
    path('stores_json_create/', views.StoreJsonCreateView.as_view()),
    path('publishers_json_create/', views.PublisherJsonCreateView.as_view()),
    path('main_books/', views.MainBookView.as_view(), name='main_books')
]
