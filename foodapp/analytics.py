from django.db.models import Sum
from .models import Order


def revenue():

    return Order.objects.aggregate(
        Sum("total_price")
    )