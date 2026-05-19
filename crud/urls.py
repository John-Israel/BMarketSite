from django.urls import path
from . import views

urlpatterns = [
    # User auth
    path('page/Log_in',  views.Log_in),
    path('page/sign_up', views.sign_up),

    # User pages
    path('page/home',    views.home),
    path('page/shop',    views.shop),
    path('page/contact', views.contact),

    # Cart (page + AJAX endpoints)
    path('page/cart',         views.cart),
    path('page/cart/add',     views.cart_add),
    path('page/cart/update',  views.cart_update),
    path('page/cart/remove',  views.cart_remove),

    # Payment
    path('page/payment', views.payment),

    # Admin
    path('admin/admin_home',           views.admin_home),
    path('admin/stack',                views.admin_stack),
    path('admin/products/update_stock', views.admin_update_stock),
    path('admin/products/delete',       views.admin_delete_product),
]