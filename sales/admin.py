from django.contrib import admin

from .models import PaymentMode, Sales
# Register your models here.
admin.site.register(Sales)
admin.site.register(PaymentMode)
