from django.core.mail import send_mail


def order_confirm(email):

    send_mail(
        "Order confirmed",
        "Your order placed successfully",
        "restaurant@gmail.com",
        [email]
    )