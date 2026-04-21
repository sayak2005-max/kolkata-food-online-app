from django.contrib import admin
from .models import Category, Menu, Customer, Order, Address

admin.site.register(Category)
admin.site.register(Menu)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Address)