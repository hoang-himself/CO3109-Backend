from django.urls import path
from .views import UserOrderView, UserCheckout

app_name = 'v1_order'

urlpatterns = [
    path('order', UserOrderView.as_view(), name='order_mgmt'),
    path('checkout', UserCheckout.as_view(), name='order_checkout'),
]
