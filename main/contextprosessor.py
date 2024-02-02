from account.models import Cart, Like


def get_my_carts(request):
    user = request.user
    if user.is_authenticated:
        carts = Cart.objects.filter(user=user)
    else:
        carts = []
    price = 0
    items = 0
    for i in carts:
        items += i.quantity
        if i.product.sale_price:
            price += i.product.sale_price
        else:
            price += i.product.price
    total = {'items': items, 'price': price}
    return {'carts': carts, 'total': total}