from django.contrib import admin
from .models import Category, Collection, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'color', 'category', 'is_available')
    list_filter = ('category', 'collections', 'is_available')
    search_fields = ('name', 'description')