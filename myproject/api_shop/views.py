from rest_framework import viewsets, pagination
from firstproject.models import Category, Collection, Product, Order
from .serializers import CategorySerializer, CollectionSerializer, ProductSerializer, OrderSerializer

class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = StandardResultsSetPagination

class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    pagination_class = StandardResultsSetPagination

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('category').prefetch_related('collections').all()
    serializer_class = ProductSerializer
    pagination_class = StandardResultsSetPagination

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.select_related('user').all()
    serializer_class = OrderSerializer
    pagination_class = StandardResultsSetPagination