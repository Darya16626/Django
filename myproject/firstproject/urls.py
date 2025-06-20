from django.urls import path
from . import views
from django.shortcuts import redirect
from .views import (
    register_view,
    login_view,
    logout_view,
    info_view,
    clients_view,
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    client_product_list,
    client_product_detail,
    add_to_cart,
    cart_view,
)

urlpatterns = [
    path('', lambda request: redirect('info_view')),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('info/', views.info_view, name='info_view'),
    path('clients/', views.clients_view, name='clients_view'),

    # Админские маршруты
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/create/', views.ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('products/<int:pk>/update/', views.ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),

    # Клиентские маршруты
    path('client/products/', views.client_product_list, name='client_product_list'),
    path('client/products/<int:pk>/', views.client_product_detail, name='client_product_detail'),
    path('client/comments/<int:comment_id>/like/', views.like_comment, name='like_comment'),
    path('client/products/<int:pk>/', views.client_product_detail, name='client_product_detail'),
    path('client/products/<int:product_id>/add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('client/cart/', views.cart_view, name='cart'),
     path('client/products/<int:pk>/', views.client_product_detail, name='client_product_detail'),
    path('client/comments/<int:comment_id>/like/', views.like_comment, name='like_comment'),
    path('client/cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('client/cart/update/<int:item_id>/', views.update_quantity, name='update_quantity'),
    path('client/checkout/', views.checkout_view, name='checkout'),
    path('client/order-success/', views.order_success_view, name='order_success'),
    path('client/history/', views.client_history_view, name='client_history'),
    path('client/add-balance/', views.add_balance, name='add_balance'),
    path('client/shipment/<int:order_id>/', views.shipment_status_view, name='shipment_status'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('info/', views.info_view, name='info_view')
]