from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

# Register your models here.
from django.contrib import admin
from .models import Product,customer,Cart,Payment,Wishlist

# Register your models here.

admin.site.register(Product)
admin.site.register(customer)
admin.site.register(Cart)
admin.site.register(Payment)
admin.site.register(Wishlist)