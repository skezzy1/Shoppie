from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('aboutUs', views.aboutUs, name="aboutUs"),
    path('cart', views.cart, name='cart'),
    path('contact', views.send_contact_view, name='send_contact_view'),
    path('subscribe', views.subscribe_newsletter, name='subscribe_newsletter'),
    #blog
    path('blog/', views.blog, name='blog'),
    path('blog/<int:post_id>/', views.blog_detail, name='blog_detail'),
    path('blog/create', views.create_blog_post, name='create_blog_post'),  
    path('blog/<int:post_id>/edit/', views.edit_blog_post, name='edit_blog_post'),
    path('blog/<int:post_id>/delete/', views.delete_blog_post, name='delete_blog_post'),
    #shop
    path('shop/', views.shop, name='shop'), 
    path('shop/<int:product_id>/', views.product_detail, name='shop_detail'), 
    path('shop/create', views.create_shop_product, name='create_shop_product'), 
    path('shop/<int:product_id>/edit/', views.edit_shop_product, name='edit_product'),  
    path('shop/<int:product_id>/delete/', views.delete_shop_product, name='delete_product'),
    #cart
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('delete_from_cart/<int:product_id>/', views.delete_from_cart, name='delete_from_cart'),
    path('increase_quantity/<int:product_id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease_quantity/<int:product_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-history/', views.order_history, name='order_history'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)