from django.urls import path
from .views import *


urlpatterns = [
    path('', index_view, name='index'),
    path('category/<int:pk>/', category_view, name='category'),
    path('product/<int:pk>/', product_item_view, name='product-item'),
    path('product_quantity/', product_quantity, name='products'),
    path('my-wishlist/', whishlist, name='wishlist'),
    path('cart/<int:pk>/', card_view, name='cart'),
]
