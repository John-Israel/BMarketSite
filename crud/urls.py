from django.urls import path
from . import views

urlpatterns = [
    path('page/Log_in', views.Log_in),
    path('page/home', views.home),
    path('page/shop', views.shop),
    path('page/cart', views.cart),
    path('page/payment', views.payment),
]