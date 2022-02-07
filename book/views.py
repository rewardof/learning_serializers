from django.db.models import Avg, Sum, Count
from django.db.models.functions import Length
from django.shortcuts import render
from .serializers import AuthorSerializer, StoreSerializer, BookCreateSerializer, PublisherSerializer, BookSerializer, \
    PriceSerializer, PublisherWithNumBookSerializer
from .models import Book, Publisher, Author, Store
from rest_framework import generics, status
from rest_framework.response import Response


class BookJsonCreateView(generics.ListCreateAPIView):
    serializer_class = BookCreateSerializer
    queryset = Book.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class AuthorJsonCreateView(generics.ListCreateAPIView):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class StoreJsonCreateView(generics.ListCreateAPIView):
    serializer_class = StoreSerializer
    queryset = Store.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class PublisherJsonCreateView(generics.ListCreateAPIView):
    serializer_class = PublisherSerializer
    queryset = Publisher.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class MainBookView(generics.ListCreateAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()

    def get(self, *args, **kwargs):
        data = self.request
        # total books count
        books_count = Book.objects.all().count()

        # books that name length is gt 32
        books_name_length_gt_ten = BookSerializer(Book.objects.annotate(lenght=Length('name')).filter(lenght__gt=32), many=True).data

        # avg price of all books
        avg_price = Book.objects.aggregate(avg_price=Avg('price'))
        # total price off all books
        total_price = PriceSerializer(Book.objects.aggregate(total_price=Sum('price'))).data

        publisher = Publisher.objects.annotate(num_books=Count('books')).values('name', 'num_books')[:3]

        book_authors_count = Book.objects.annotate(num_authors=Count('authors')).values('name', 'num_authors')[:3]

        books_author_26 = Book.objects.filter(authors__in=(26, 11, 12)).count()

        payload = {
            'books_count': books_count,
            'books_name_length_gt_ten': books_name_length_gt_ten,
            'avg_price': avg_price,
            'total_price': total_price,
            'publisher': publisher,
            'book_authors': book_authors_count,
            'books_author_26': books_author_26,
        }
        return Response(payload, status=status.HTTP_200_OK)
