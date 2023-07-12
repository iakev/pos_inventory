from django.contrib import admin

from .models import Supplier, Business, Employee

# Register your models here.
admin.site.register(Supplier)
admin.site.register(Business)
admin.site.register(Employee)
