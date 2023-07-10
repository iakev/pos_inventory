from django.contrib import admin

from .models import Supplier, Customer, Business, Employee
# Register your models here.
admin.site.register(Supplier)
admin.site.register(Customer)
admin.site.register(Business)
admin.site.register(Employee)
