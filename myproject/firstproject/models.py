from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, Group, Permission

MAX_LENGTH = 255

class Role(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class User(AbstractUser):
    roles = models.ManyToManyField('Role', through='UserRole')
    balance = models.FloatField(default=0.0)

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',
        blank=True,
        help_text='Группы, к которым принадлежит пользователь.',
        verbose_name='группы',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set',
        blank=True,
        help_text='Разрешения, предоставленные пользователю.',
        verbose_name='разрешения пользователя',
    )

class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

class Category(models.Model):
    name = models.CharField(max_length=MAX_LENGTH)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Collection(models.Model):
    name = models.CharField(max_length=MAX_LENGTH)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    name = models.CharField(max_length=MAX_LENGTH)
    description = models.TextField(null=True, blank=True)
    price = models.FloatField()
    color = models.CharField(max_length=MAX_LENGTH)
    photo = models.ImageField(upload_to='products/%Y/%m/%d', null=True, blank=True)
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, blank=True)
    collections = models.ManyToManyField(Collection, through='ProductCollection', blank=True)

    def __str__(self):
        return self.name

class ProductCollection(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)

class Order(models.Model):
    STATUS_CHOICES = (
        ('new', 'Новый'),
        ('processing', 'В обработке'),
        ('shipped', 'Отправлен'),
        ('completed', 'Завершён'),
        ('cancelled', 'Отменён'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"Заказ #{self.id} пользователя {self.user.username}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"

    def get_cost(self):
        return self.product.price * self.quantity
    
class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = (
        ('card', 'Банковская карта'),
        ('cash', 'Наличные'),
        ('online', 'Онлайн-оплата'),
    )
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    amount = models.FloatField()
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=MAX_LENGTH, choices=PAYMENT_METHOD_CHOICES)

    def __str__(self):
        return f"Оплата заказа #{self.order.id} на сумму {self.amount}"

class Shipment(models.Model):
    DELIVERY_STATUS_CHOICES = (
        ('pending', 'В ожидании'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменён'),
    )
    order = models.OneToOneField('Order', on_delete=models.CASCADE)
    address = models.TextField()
    shipped_date = models.DateTimeField(null=True, blank=True)
    delivery_status = models.CharField(max_length=MAX_LENGTH, choices=DELIVERY_STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Доставка заказа #{self.order.id} - {self.delivery_status}"

class Stock(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

class Log(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=MAX_LENGTH)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)

class KeyData(models.Model):
    key = models.CharField(max_length=MAX_LENGTH, unique=True)
    description = models.TextField(null=True, blank=True)

class KeyDataRole(models.Model):
    keydata = models.ForeignKey(KeyData, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

class Comment(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Комментарий от {self.user.username} к {self.product.name}"

class CommentLike(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('comment', 'user')  # Один пользователь может лайкнуть комментарий только один раз

    class Meta:
        unique_together = ('comment', 'user')  # Один пользователь может лайкнуть комментарий только один раз