from django.db import models

class Image(models.Model):
    image = models.ImageField(upload_to='%Y/%m/%d/')
    created_at = models.DateTimeField(auto_now_add=True)


class Category(models.Model):
    name = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=32)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='sub_categories')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category.name} -> {self.name}"


class Product(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    status = models.IntegerField(default=0, choices=(
        (0, 'In Progress'),
        (1, 'Completed'),
        (2, 'Deleted')
    ))
    image = models.ManyToManyField(Image, blank=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='products')
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"

    def set_sale_percent(self, percent: int) -> None:
        price = self.price - (self.price / 100 * percent)
        self.sale_price = price
        self.save()


class ProductQuantity(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='quantity')
    quantity = models.IntegerField(default=0)
    size = models.IntegerField(default=0, choices=(
        (0, 'Large'),
        (1, 'X-Large'),
        (2, 'XX-Large'),
    ))
    color = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.title}"










