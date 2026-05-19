from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
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
    path('page/cart/add/<int:productId>/',     views.cart_add),
    path('page/cart/update',  views.cart_update),
    path('page/cart/remove',  views.cart_remove),

    # Payment
    path('page/payment', views.payment),

    # admin authentication and page navigation for admin
    path('admin/admin_home', views.admin_home),
    path('admin/product_list', views.product_list),
    path('admin/add_product', views.add_product),
    path('admin/delete_product/<int:id>', views.delete_product),
    path('admin/update_product/<int:productId>', views.update_product),
    path('admin/user_list', views.user_list),
]   + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
