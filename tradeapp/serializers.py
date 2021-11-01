from rest_framework import serializers
from .models import Item, Customer, Purchase


class AddItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = '__all__'

    def create(self, validated_data):
        print(validated_data)
        user = super(AddItemSerializer, self).create(validated_data)
        return user


class AddCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class AddPurchaseSerializer(serializers.ModelSerializer):
    item = serializers.SlugRelatedField(queryset=Item.objects.all(), slug_field='name')
    customer = serializers.SlugRelatedField(queryset=Customer.objects.all(), slug_field='name')

    class Meta:
        model = Purchase
        fields = '__all__'
