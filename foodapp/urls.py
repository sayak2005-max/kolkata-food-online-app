from django.urls import path
from . import views


urlpatterns = [

path("", views.login_page),

path("home/", views.home),

path("about/", views.about),

path("order/", views.order),

path("checkout/", views.checkout),

path("user-login/", views.user_login),

path("profile/", views.profile),

path("order-history/", views.order_history),

path("dashboard/", views.dashboard),

path("review/<int:item_id>/", views.review),

path("add-address/", views.add_address),

path("logout/", views.user_logout),

]