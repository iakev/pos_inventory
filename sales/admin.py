from django.contrib import admin

from .models import PaymentMode, Sales, Customer, ProductSales

# Register your models here.
admin.site.register(Sales)
admin.site.register(PaymentMode)
admin.site.register(Customer)
admin.site.register(ProductSales)
