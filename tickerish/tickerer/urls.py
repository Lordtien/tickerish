from django.urls import path

from . import views

urlpatterns = [
    path('exchange-rate/', views.get_exchange_rate, name='exchange-rate'),
]
