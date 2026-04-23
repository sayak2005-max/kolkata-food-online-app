from django.contrib import admin
from .models import Customer, Category, Menu, Order, Review, Address


# CUSTOMER ADMIN

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):

    list_display = (

        "user",

        "mobile",

        "address"

    )



# CATEGORY ADMIN

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = ("name",)



# MENU ADMIN

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):

    list_display = (

        "name",

        "category",

        "price",

        "is_veg",

        "is_available"

    )

    list_filter = (

        "category",

        "is_veg",

        "is_available"

    )



# ORDER ADMIN (IMPORTANT SECTION)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (

        "customer",

        "item",

        "quantity",

        "delivery_type",

        "status",

        "total_price",

        "created_at"

    )

    list_filter = (

        "status",

        "delivery_type",

        "created_at"

    )

    search_fields = (

        "customer__mobile",

        "item__name"

    )



# REVIEW ADMIN

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    list_display = (

        "user",

        "item",

        "rating"

    )



# ADDRESS ADMIN

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):

    list_display = (

        "customer",

        "city",

        "pincode"

    )