from django.urls import path
from django.views.generic import RedirectView
from .views import info_view

urlpatterns = [
    path('', RedirectView.as_view(url='info/', permanent=False)),  # перенаправление с корня на /info/
    path('info/', info_view, name='info_view'),
]