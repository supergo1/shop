from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser

from main.models import *


def rating_validator(value):
    if 0 <= value <= 5:
        return value
    else:
        raise ValidationError('0dan 5gacha baholang!')


class User(AbstractUser):
    phone = models.CharField(max_length=20)
    status = models.IntegerField(default=0, choices=(
        (0, 'Client'),
        (1, 'Admin')
    ))

    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"
        swappable = 'AUTH_USER_MODEL'


class Address(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='address')
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    house_number = models.IntegerField(default=0)
    postal_code = models.CharField(max_length=20)

    def __str__(self):
        return self.user.get_full_name()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} -> {self.product.title}"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='carts')
    quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()}"


class Checkout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='checkouts')
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, related_name='checkout')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()}"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    comment = models.TextField()
    rating = models.IntegerField(default=0, validators=[rating_validator])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()}"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)








