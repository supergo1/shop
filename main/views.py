from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from account.models import Review
from .models import *
from account.models import *


@login_required(login_url='login')
def index_view(request):
    categories = Category.objects.all()
    latest_products = Product.objects.all().order_by('-id')[:5]
    rating = Product.objects.all().order_by('reviews__rating')[:3]
    context = {
        'categories': categories,
        'latest_products': latest_products,
        'rating': rating
    }
    return render(request, 'index.html', context)


def category_view(request, pk):
    category = Category.objects.get(id=pk)
    sub_categories = category.sub_categories.all()
    products = []
    for sub_category in sub_categories:
        products.extend(list(Product.objects.filter(sub_category=sub_category).order_by('-id')))
    context = {
        'sub_categories': sub_categories,
        'products': products[:9]
    }
    print(products)
    return render(request, 'category.html', context)


def sorter(lugat):
    tartiblangan_items = sorted(lugat.items(), key=lambda x: x[1])
    tartiblangan_lugat = dict(tartiblangan_items)
    return tartiblangan_lugat


def product_item_view(request, pk):
    a = request.resolver_match.view_name
    product = Product.objects.get(id=pk)
    action = request.GET.get('action')
    quantity = request.POST.get('quantity')
    if action == 'like':
        like = Like.objects.create(user=request.user, product=product)
        return redirect(a, pk=product.id)
    if action == 'dislike':
        like = Like.objects.get(user=request.user, product=product)
        like.delete()
        return redirect(a, pk=product.id)
    popular_products = Product.objects.all().order_by('likes')[:5]
    sub_categories = SubCategory.objects.filter(category=product.sub_category.category)
    all_product = Product.objects.all()
    is_like = Like.objects.filter(product=product, user=request.user)

    best_seller = {}
    for product1 in all_product:
        for cart in product1.carts.all():
            try:
                if best_seller.get(str(product1.id)) is not None:
                    best_seller[str(product1.id)] += cart.quantity
                else:
                    best_seller[str(product1.id)] = cart.quantity
            except Exception as e:
                print(e)
    a = sorter(best_seller)
    z = list((a if len(a) < 5 else dict(list(a.items())[:5])).keys())
    print([Product.objects.get(id=int(x)) for x in z])
    context = {
        'product': product,
        'popular_products': popular_products,
        'sub_categories': sub_categories,
        'best_seller': [Product.objects.get(id=int(x)) for x in z],
        'like': is_like
    }
    return render(request, 'product-item.html', context)


def product_quantity(request):
    context = {
        'products': ProductQuantity.objects.all()
    }
    return render(request, 'base.html', context)


def dislike(request):
    user = request.user
    action = request.GET.get('action')
    liked_product = Like.objects.get(user=user, product=product.id)
    if action == 'dislike':
        redirect('wishlist')
        liked_product.delete
    else:
        pass
    Like.save


def whishlist(request):
    user = request.user
    likes = Like.objects.filter(user=user)
    like_id = request.GET.get('like_id')
    if like_id:
        like = Like.objects.get(id=like_id).delete()
        return redirect('wishlist')
    context = {
        'likes': likes
    }
    return render(request, 'shop-wishlist.html', context)


def card_view(request, pk):
    action = request.GET.get('action')
    product = Product.objects.get(id=pk)
    carts = Cart.objects.filter(user=request.user)
    cart = Cart.objects.get(user=request.user, product=product)
    if action == 'delete':
        cart.delete()
        return redirect('index')
    elif action == 'addtocart':
        quantity = request.GET.get('quantity')
        Cart.objects.create(user=request.user, product=product, quantity=2)
        return redirect('product-item', pk=product.id)

