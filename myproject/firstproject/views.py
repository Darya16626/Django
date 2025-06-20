from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Product
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Product, Comment, CommentLike
from .forms import CommentForm
from .models import Product, Order, OrderItem, Log
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, Payment, Shipment
from .forms import OrderCreateForm
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Order, Payment, Shipment
from .forms import OrderCreateForm

from .forms import ProductForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import Product, Comment, CommentLike
from .forms import CommentForm

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Product, Comment, CommentLike
from .forms import CommentForm
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .forms import UserRegisterForm, UserLoginForm
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Order, OrderItem
from django.db.models import Q
from .forms import ProductSearchForm
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .models import Log

from .models import Product, Order, OrderItem
from .forms import (
    ProductSearchForm, UserRegisterForm, UserLoginForm,
    ProductForm, OrderCreateForm
)

@login_required
def client_history_view(request):
    logs = Log.objects.filter(user=request.user).order_by('-timestamp')
    orders = Order.objects.filter(user=request.user).order_by('-created_at').prefetch_related('shipment')
    return render(request, 'client_history.html', {'logs': logs, 'orders': orders})

@login_required
@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_available=True)
    order, created = Order.objects.get_or_create(user=request.user, status='new')
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
    if not created:
        order_item.quantity += 1
        order_item.save()
    return redirect('cart')  # Перенаправляем сразу в корзину

@login_required
def client_product_list(request):
    form = ProductSearchForm(request.GET or None)
    products = Product.objects.filter(is_available=True)

    if form.is_valid():
        name = form.cleaned_data.get('name')
        color = form.cleaned_data.get('color')
        price_min = form.cleaned_data.get('price_min')
        price_max = form.cleaned_data.get('price_max')

        if name:
            products = products.filter(name__icontains=name)
        if color:
            products = products.filter(color__icontains=color)
        if price_min is not None:
            products = products.filter(price__gte=price_min)
        if price_max is not None:
            products = products.filter(price__lte=price_max)

    return render(request, 'client_product/product_list.html', {'products': products, 'form': form})

@login_required
def client_product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, is_available=True)
    comments = product.comments.select_related('user').prefetch_related('likes').order_by('-created_at')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            Comment.objects.create(
                product=product,
                user=request.user,
                text=form.cleaned_data['text']
            )
            return redirect('client_product_detail', pk=pk)
    else:
        form = CommentForm()

    comments_with_likes = []
    for comment in comments:
        liked_by_user = comment.likes.filter(user=request.user).exists()
        comments_with_likes.append({
            'comment': comment,
            'likes_count': comment.likes.count(),
            'liked_by_user': liked_by_user,
        })

    context = {
        'product': product,
        'form': form,
        'comments_with_likes': comments_with_likes,
    }
    return render(request, 'client_product/product_detail.html', context)

@login_required
@require_POST
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    liked, created = CommentLike.objects.get_or_create(comment=comment, user=request.user)
    if not created:
        liked.delete()
        liked_status = False
    else:
        liked_status = True
    return JsonResponse({
        'liked': liked_status,
        'likes_count': comment.likes.count(),
    })

@login_required
@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_available=True)
    order, created = Order.objects.get_or_create(user=request.user, status='new')
    order_item, item_created = OrderItem.objects.get_or_create(order=order, product=product)
    if not item_created:
        order_item.quantity += 1
        order_item.save()
    # Логируем действие
    Log.objects.create(
        user=request.user,
        action='Добавление в корзину',
        description=f'Товар: {product.name}'
    )
    messages.success(request, f"Добавлен товар: {product.name}")
    return redirect('cart')

@login_required
def cart_view(request):
    order = Order.objects.filter(user=request.user, status='new').first()
    items = []
    total = 0
    if order:
        items = order.items.all()
        for item in items:
            item.total_price = item.product.price * item.quantity
        total = sum(item.total_price for item in items)
    return render(request, 'cart.html', {'order': order, 'items': items, 'total': total})

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Перенаправление после регистрации
            if user.is_superuser:
                return redirect('info_view')
            else:
                return redirect('clients_view')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Если суперпользователь — редирект на info
            if user.is_superuser:
                return redirect('info_view')
            else:
                return redirect('clients_view')  # Или куда нужно для обычных пользователей
        else:
            messages.error(request, "Неверное имя пользователя или пароль.")
    else:
        form = UserLoginForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def info_view(request):
    # Страница админа
    if not request.user.is_superuser:
        return redirect('clients_view')
    return render(request, 'info.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if user.is_superuser:
                return redirect('info_view')
            else:
                return redirect('clients_view')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def cart_view(request):
    order = Order.objects.filter(user=request.user, status='new').first()
    items = []
    total = 0
    if order:
        items = order.items.all()
        for item in items:
            item.total_price = item.product.price * item.quantity  # вычисляем сумму для позиции
        total = sum(item.total_price for item in items)  # общая сумма
    return render(request, 'cart.html', {'order': order, 'items': items, 'total': total})

@login_required
def clients_view(request):
    # Страница для клиентов
    if request.user.is_superuser:
        return redirect('info_view')
    return render(request, 'clients.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def info_view(request):
    return render(request, 'info.html')

class ProductListView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'product/product_list.html'

class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'product/product_detail.html'

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/product_form.html'
    success_url = reverse_lazy('product_list')

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/product_form.html'
    success_url = reverse_lazy('product_list')

class ProductDeleteView(DeleteView):
    model = Product
    context_object_name = 'product'
    template_name = 'product/product_delete.html'
    success_url = reverse_lazy('product_list')

@login_required
@require_POST
def remove_from_cart(request, item_id):
    order_item = get_object_or_404(OrderItem, id=item_id, order__user=request.user, order__status='new')
    order_item.delete()
    messages.info(request, "Товар удалён из корзины.")
    return redirect('cart')

@login_required
@require_POST
def update_quantity(request, item_id):
    order_item = get_object_or_404(OrderItem, id=item_id, order__user=request.user, order__status='new')
    try:
        quantity = int(request.POST.get('quantity', 1))
    except ValueError:
        quantity = 1
    if quantity > 0:
        order_item.quantity = quantity
        order_item.save()
        messages.success(request, "Количество обновлено.")
    else:
        order_item.delete()
        messages.info(request, "Товар удалён из корзины.")
    return redirect('cart')

@login_required
def checkout_view(request):
    order = Order.objects.filter(user=request.user, status='new').first()
    if not order or order.items.count() == 0:
        messages.warning(request, "Ваша корзина пуста.")
        return redirect('cart')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order.address = form.cleaned_data['address']
            order.phone = form.cleaned_data['phone']
            order.status = 'processing'
            order.save()

            Payment.objects.create(
                order=order,
                amount=order.get_total_cost(),
                payment_method=form.cleaned_data['payment_method']
            )

            Shipment.objects.create(
                order=order,
                address=order.address,
                delivery_status='pending'
            )

            messages.success(request, "Заказ оформлен! Мы свяжемся с вами.")
            return redirect('order_success')
    else:
        form = OrderCreateForm()

    return render(request, 'checkout.html', {'order': order, 'form': form})

@login_required
def order_success_view(request):
    return render(request, 'order_success.html')


@login_required
@require_POST
def add_balance(request):
    amount = request.POST.get('amount')
    try:
        amount = float(amount)
        if amount <= 0:
            raise ValueError
    except (ValueError, TypeError):
        messages.error(request, "Введите корректную сумму для пополнения.")
        return redirect('clients_view')

    user = request.user
    user.balance += amount
    user.save()
    messages.success(request, f"Баланс успешно пополнен на {amount} рублей.")
    return redirect('clients_view')

@login_required
def shipment_status_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    shipment = getattr(order, 'shipment', None)
    if not shipment:
        messages.warning(request, "Информация о доставке для этого заказа отсутствует.")
        return redirect('client_history')

    return render(request, 'shipment_status.html', {'shipment': shipment, 'order': order})