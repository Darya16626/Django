from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Product, Collection
from .models import Order, Payment, Shipment

class CommentForm(forms.Form):
    text = forms.CharField(
        label='Оставить комментарий',
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Ваш комментарий...'}),
        max_length=1000,
        required=True
    )

class ProductSearchForm(forms.Form):
    name = forms.CharField(required=False, label='Название', widget=forms.TextInput(attrs={'placeholder': 'Название'}))
    color = forms.CharField(required=False, label='Цвет', widget=forms.TextInput(attrs={'placeholder': 'Цвет'}))
    price_min = forms.FloatField(required=False, label='Минимальная цена', min_value=0)
    price_max = forms.FloatField(required=False, label='Максимальная цена', min_value=0)

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(widget=forms.PasswordInput)

class ProductForm(forms.ModelForm):
    collections = forms.ModelMultipleChoiceField(
        queryset=Collection.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'color', 'photo', 'is_available', 'category', 'collections']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class OrderCreateForm(forms.Form):
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), label='Адрес доставки')
    phone = forms.CharField(max_length=20, label='Телефон для связи')
    payment_method = forms.ChoiceField(
        choices=Payment.PAYMENT_METHOD_CHOICES,
        label='Метод оплаты',
        widget=forms.RadioSelect
    )