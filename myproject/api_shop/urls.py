from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, CollectionViewSet, ProductViewSet, OrderViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='category')
router.register('collections', CollectionViewSet, basename='collection')
router.register('products', ProductViewSet, basename='product')
router.register('orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
]