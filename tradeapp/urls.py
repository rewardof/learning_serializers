from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tradeapp import views

router = DefaultRouter()
router.register('items', views.ItemViewSet, basename='items')
router.register('customers', views.CustomerViewSet, basename='customers')
router.register('purchase', views.PurchaseViewSet, basename='purchase')

urlpatterns = [
    path('', include(router.urls)),
]
