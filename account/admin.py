from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(Checkout)
admin.site.register(Review)
admin.site.register(Like)
