from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='blog-Home'),
    path('subpage/<int:post_id>', views.subpage, name='blog-Subpage'),
    path('about/', views.about, name='blog-About'),
    path('cart/', views.cart, name='blog-Cart'),
    path('newReleases/', views.newReleases, name='blog-newReleases'),
    path('cat_find/<int:category_id>', views.cat_find, name='cat_find-Home'),
    path('add_to_cart/', views.add_to_cart_view, name='add_to_cart'),
    path('remove_from_cart/', views.remove_from_cart_view, name='remove_from_cart'),
    path('change_item_qty/', views.change_item_qty, name='change_item_qty'),
    path('cart/', views.cart_view, name='cart'),

]
