from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.conf import settings

from .models import Customer, Menu, Order, Review, Address

import json


# HOME PAGE

@login_required(login_url="/")
def home(request):

    return render(request, "home.html")


# ABOUT PAGE

def about(request):

    return render(request, "about.html")


# ORDER PAGE

@login_required(login_url="/")
def order(request):

    menu = Menu.objects.filter(
        is_available=True
    ).select_related("category")

    return render(request, "order.html", {"menu": menu})


# CHECKOUT PAGE

@login_required(login_url="/")
def checkout(request):

    if request.method == "POST":

        cart_data = request.POST.get("cart_data")

        if not cart_data:

            return redirect("/order/")

        cart = json.loads(cart_data)

        request.session["cart"] = cart


    cart = request.session.get("cart", [])

    if not cart:

        return redirect("/order/")


    total = sum(

        item["price"] * item["quantity"]

        for item in cart

    )


    from .payments import create_order

    razorpay_order = create_order(total)


    return render(

        request,

        "payment.html",

        {

            "razorpay_key": settings.RAZORPAY_KEY_ID,

            "amount": razorpay_order["amount"],

            "razorpay_order_id": razorpay_order["id"],

            "total": total

        }

    )

@login_required(login_url="/")
def payment_page(request):

    cart = request.session.get("cart", [])

    if not cart:
        return redirect("/order/")

    total = sum(
        item["price"] * item["quantity"]
        for item in cart
    )

    from .payments import create_order

    razorpay_order = create_order(total)

    return render(
        request,
        "payment.html",
        {
            "razorpay_key": settings.RAZORPAY_KEY_ID,
            "amount": razorpay_order["amount"],
            "razorpay_order_id": razorpay_order["id"],
            "total": total
        }
    )


# PAYMENT SUCCESS

@login_required(login_url="/")
def payment_success(request):

    if request.method == "POST":

        razorpay_order_id = request.POST.get("razorpay_order_id")

        payment_id = request.POST.get("razorpay_payment_id")

        signature = request.POST.get("razorpay_signature")

        from .payments import verify_payment

        if verify_payment(
            razorpay_order_id,
            payment_id,
            signature
        ):

            cart = request.session.get("cart", [])

            address = request.session.get("address", "")

            customer, _ = Customer.objects.get_or_create(
                user=request.user,
                defaults={"mobile": request.user.username}
            )

            customer.address = address
            customer.save()

            for item in cart:

                menu_item = Menu.objects.get(name=item["name"])

                Order.objects.create(
                    customer=customer,
                    item=menu_item,
                    quantity=item["quantity"],
                    total_price=item["price"] * item["quantity"]
                )

            request.session.pop("cart", None)
            request.session.pop("address", None)
            request.session.pop("razorpay_order_id", None)

            return redirect("/tracking/")

        else:

            return render(request, "payment_failed.html")

    return redirect("/")


# TRACKING PAGE

@login_required(login_url="/")
def tracking(request):

    customer, _ = Customer.objects.get_or_create(
        user=request.user,
        defaults={"mobile": request.user.username}
    )

    orders = Order.objects.filter(
        customer=customer
    ).order_by("-created_at")

    return render(
        request,
        "tracking.html",
        {"orders": orders}
    )


# LOGIN PAGE

def login_page(request):

    if request.user.is_authenticated:
        return redirect("/home/")

    return render(request, "login.html")


# MOBILE LOGIN SYSTEM

def user_login(request):

    if request.method == "POST":

        mobile = request.POST.get("mobile")

        customer = Customer.objects.filter(
            mobile=mobile
        ).first()

        if customer:

            login(request, customer.user)

        else:

            user = User.objects.create(username=mobile)

            Customer.objects.create(
                user=user,
                mobile=mobile
            )

            login(request, user)

        return redirect("/home/")

    return render(request, "user_login.html")


# REVIEW SYSTEM

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


# ORDER HISTORY

@login_required(login_url="/")
def order_history(request):

    customer, _ = Customer.objects.get_or_create(
        user=request.user,
        defaults={"mobile": request.user.username}
    )

    orders = Order.objects.filter(customer=customer)

    return render(
        request,
        "order_history.html",
        {"orders": orders}
    )


# PROFILE PAGE

@login_required(login_url="/")
def profile(request):

    customer, _ = Customer.objects.get_or_create(
        user=request.user,
        defaults={"mobile": request.user.username}
    )

    addresses = Address.objects.filter(customer=customer)

    return render(
        request,
        "profile.html",
        {
            "customer": customer,
            "addresses": addresses
        }
    )


# ADD ADDRESS

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


# DASHBOARD

@login_required(login_url="/")
def dashboard(request):

    revenue = Order.objects.aggregate(Sum("total_price"))

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


# LOGOUT

def user_logout(request):

    logout(request)

    return redirect("/")