import razorpay
from django.conf import settings


client = razorpay.Client(
    auth=(
        settings.RAZORPAY_KEY_ID,
        settings.RAZORPAY_KEY_SECRET
    )
)


def create_order(amount):

    data = {

        "amount": int(amount) * 100,  # convert ₹ to paise

        "currency": "INR",

        "payment_capture": "1"

    }

    return client.order.create(data=data)


def verify_payment(order_id, payment_id, signature):

    params_dict = {

        "razorpay_order_id": order_id,

        "razorpay_payment_id": payment_id,

        "razorpay_signature": signature

    }

    try:

        client.utility.verify_payment_signature(params_dict)

        return True

    except:

        return False