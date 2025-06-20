from rest_framework import serializers
from firstproject.models import Category, Collection, Product, Order

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'name', 'description']

class ProductSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(use_url=True, allow_null=True, required=False)
    category = CategorySerializer(read_only=True)
    collections = CollectionSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'color',
            'photo', 'is_available', 'category', 'collections'
        ]

class OrderSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d.%m.%Y %H:%M', read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at', 'status', 'address', 'phone']