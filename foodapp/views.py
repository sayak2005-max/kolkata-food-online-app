from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from .models import Customer, Menu, Order, Review

import json


# ---------------- HOME PAGE ----------------

@login_required(login_url="/")
def home(request):

    return render(request, "home.html")


# ---------------- ABOUT PAGE ----------------

def about(request):

    return render(request, "about.html")


# ---------------- ORDER PAGE ----------------

@login_required(login_url="/")
def order(request):

    menu = Menu.objects.filter(
        is_available=True
    ).select_related("category")

    return render(
        request,
        "order.html",
        {"menu": menu}
    )


# ---------------- CHECKOUT ----------------

@login_required(login_url="/")
def checkout(request):

    if request.method == "POST":

        cart_data = request.POST.get("cart_data")

        if not cart_data:

            return redirect("/order/")

        cart = json.loads(cart_data)

        customer, created= Customer.objects.get_or_create(
            user=request.user,
            defaults={
                "mobile": request.user.username
            }
        )

        for item in cart:

            menu_item = Menu.objects.get(
                name=item["name"]
            )

            Order.objects.create(

                customer=customer,

                item=menu_item,

                quantity=item["quantity"],

                total_price=item["price"]
                * item["quantity"]

            )

        return render(
            request,
            "success.html"
        )

    return redirect("/order/")


# ---------------- LOGIN PAGE ----------------

def login_page(request):

    if request.user.is_authenticated:

        return redirect("/home/")

    return render(
        request,
        "login.html"
    )


# ---------------- MOBILE LOGIN SYSTEM ----------------

def user_login(request):

    if request.method == "POST":

        mobile = request.POST.get("mobile")

        customer = Customer.objects.filter(
            mobile=mobile
        ).first()

        if customer:

            login(
                request,
                customer.user
            )

        else:

            user = User.objects.create(
                username=mobile
            )

            Customer.objects.create(
                user=user,
                mobile=mobile
            )

            login(
                request,
                user
            )

        return redirect("/home/")

    return render(
        request,
        "user_login.html"
    )


# ---------------- REVIEW SYSTEM ----------------

@login_required(login_url="/")
def review(request, item_id):

    if request.method == "POST":

        rating = request.POST.get("rating")

        comment = request.POST.get("comment")

        Review.objects.create(

            user=request.user,

            item_id=item_id,

            rating=rating,

            comment=comment

        )

    return redirect("/order/")


# ---------------- ORDER HISTORY ----------------

@login_required(login_url="/")
def order_history(request):

    customer, _ = Customer.objects.get_or_create(
    user=request.user,
    defaults={"mobile": request.user.username}
)

    orders = Order.objects.filter(
        customer=customer
    )

    return render(

        request,

        "order_history.html",

        {"orders": orders}

    )


# ---------------- USER PROFILE ----------------

@login_required(login_url="/")
def profile(request):

    customer, _ = Customer.objects.get_or_create(
        user=request.user,
        defaults={"mobile": request.user.username}
    )

    addresses = customer.addresses.all()

    return render(
        request,
        "profile.html",
        {
            "customer": customer,
            "addresses": addresses
        }
    )

# ---------------- ADMIN DASHBOARD ----------------

@login_required(login_url="/")
def dashboard(request):

    revenue = Order.objects.aggregate(
        Sum("total_price")
    )

    orders = Order.objects.count()

    customers = Customer.objects.count()

    return render(

        request,

        "dashboard.html",

        {

            "revenue": revenue,

            "orders": orders,

            "customers": customers

        }

    )
@login_required(login_url="/")
def add_address(request):

    if request.method == "POST":

        address = request.POST.get("address")
        city = request.POST.get("city")
        pincode = request.POST.get("pincode")

        customer, _ = Customer.objects.get_or_create(
            user=request.user,
            defaults={"mobile": request.user.username}
        )

        Address.objects.create(
            customer=customer,
            address=address,
            city=city,
            pincode=pincode
        )

    return redirect("/profile/")

def user_logout(request):

    logout(request)

    return redirect("/")