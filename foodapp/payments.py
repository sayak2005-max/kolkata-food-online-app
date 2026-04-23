import razorpay
from django.conf import settings


# Razorpay client setup

client = razorpay.Client(
    auth=(
        settings.RAZORPAY_KEY_ID,
        settings.RAZORPAY_KEY_SECRET
    )
)


# CREATE ORDER FUNCTION

def create_order(amount):

    try:

        data = {

            "amount": int(amount) * 100,  # convert ₹ to paise

            "currency": "INR",

            "payment_capture": 1

        }

        return client.order.create(data=data)

    except Exception as e:

        print("Razorpay connection failed:", e)

        # fallback offline order object

        return {

            "id": "offline_order",

            "amount": int(amount) * 100

        }


# VERIFY PAYMENT FUNCTION

def verify_payment(order_id, payment_id, signature):

    params_dict = {

        "razorpay_order_id": order_id,

        "razorpay_payment_id": payment_id,

        "razorpay_signature": signature

    }

    try:

        client.utility.verify_payment_signature(params_dict)

        return True

    except Exception as e:

        print("Payment verification failed:", e)

        return False