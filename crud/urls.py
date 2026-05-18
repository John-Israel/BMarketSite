from django.urls import path
from . import views

urlpatterns = [
    # user authentication and page navigation for users
    path('page/Log_in', views.Log_in),
    path('page/sign_up', views.sign_up),
    path('page/home', views.home),
    path('page/shop', views.shop),
    path('page/cart', views.cart),
    path('page/payment', views.payment),

    # admin authentication and page navigation for admin
    path('admin/admin_home', views.admin_home),
]