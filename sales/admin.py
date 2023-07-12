from django.contrib import admin

from .models import PaymentMode, Sales, Customer

# Register your models here.
admin.site.register(Sales)
admin.site.register(PaymentMode)
admin.site.register(Customer)
