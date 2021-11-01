from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from .serializers import AddItemSerializer, AddCustomerSerializer, AddPurchaseSerializer
from .models import Item, Customer, Purchase


class ItemViewSet(ModelViewSet):
    serializer_class = AddItemSerializer
    queryset = Item.objects.all()


class CustomerViewSet(ModelViewSet):
    serializer_class = AddCustomerSerializer
    queryset = Customer.objects.all()


class PurchaseViewSet(ModelViewSet):
    serializer_class = AddPurchaseSerializer
    queryset = Purchase.objects.all()
