from rest_framework import serializers
from .models import Book, Publisher, Store, Author


class BookListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        # books = [Book(**item) for item in validated_data]
        for item in validated_data:
            authors = item.pop('authors')
            print(item)
            instance = Book(**item)
            instance.save()
            for author in authors:
                instance.authors.add(author)
            instance.save()
        return Book.objects.all()


class BookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('name', 'pages', 'price', 'rating', 'authors', 'publisher', 'pubdate')
        list_serializer_class = BookListSerializer


class PublisherListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        publishers = [Publisher(**item) for item in validated_data]
        return Publisher.objects.bulk_create(publishers)


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ('name',)
        list_serializer_class = PublisherListSerializer


class StoreListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        stores = [Store(**item) for item in validated_data]
        return Store.objects.bulk_create(stores)


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ('name', 'books')
        list_serializer_class = StoreListSerializer


class AuthorListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        authors = [Author(**item) for item in validated_data]
        return Author.objects.bulk_create(authors)


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('age', 'name')
        list_serializer_class = AuthorListSerializer


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class PriceSerializer(serializers.Serializer):
    total_price = serializers.DecimalField(decimal_places=1, max_digits=10)


class PublisherWithNumBookSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    num_books = serializers.IntegerField()
