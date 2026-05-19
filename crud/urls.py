from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
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
    path('admin/product_list', views.product_list),
    path('admin/add_product', views.add_product),
    path('admin/delete_product/<int:id>', views.delete_product),
    path('admin/update_product/<int:productId>', views.update_product),
    path('admin/user_list', views.user_list),
]   + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)