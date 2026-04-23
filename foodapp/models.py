from django.db import models
from django.contrib.auth.models import User


# CUSTOMER MODEL

class Customer(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    mobile = models.CharField(
        max_length=10,
        unique=True
    )

    address = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return self.mobile


# CATEGORY MODEL

class Category(models.Model):

    name = models.CharField(
        max_length=100
    )

    def __str__(self):
        return self.name


# MENU MODEL

class Menu(models.Model):

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )

    name = models.CharField(
        max_length=100
    )

    price = models.IntegerField()

    description = models.TextField(
        blank=True,
        null=True
    )

    image = models.ImageField(
        upload_to="menu_images/",
        blank=True,
        null=True
    )

    is_available = models.BooleanField(
        default=True
    )

    is_veg = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.name


# ORDER MODEL (UPDATED VERSION)

class Order(models.Model):

    STATUS = (
        ("Preparing", "Preparing"),
        ("Ready", "Ready"),
        ("Out for delivery", "Out for delivery"),
        ("Delivered", "Delivered"),
    )

    DELIVERY_TYPE = (
        ("self", "Self Pickup"),
        ("home", "Home Delivery"),
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE
    )

    item = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE
    )

    quantity = models.IntegerField()

    special_note = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    delivery_type = models.CharField(
        max_length=10,
        choices=DELIVERY_TYPE,
        default="self"
    )

    total_price = models.IntegerField()

    status = models.CharField(
        max_length=30,
        choices=STATUS,
        default="Preparing"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.customer} - {self.item}"


# REVIEW MODEL

class Review(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    item = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE
    )

    rating = models.IntegerField()

    comment = models.TextField()

    def __str__(self):
        return f"{self.user} - {self.item}"


# ADDRESS MODEL

class Address(models.Model):

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="addresses"
    )

    address = models.TextField()

    city = models.CharField(
        max_length=100
    )

    pincode = models.CharField(
        max_length=10
    )

    def __str__(self):
        return f"{self.customer} - {self.city}"