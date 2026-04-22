from django.core.mail import send_mail


def order_confirm(email):

    send_mail(
        "Order confirmed",
        "Your order has been placed successfully. Track it here: /tracking/",
        "restaurant@gmail.com",
        [email]
    )