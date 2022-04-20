from django.urls import path
from .views import (
    edit_or_create_order, view_order, get_self_orders, delete_order,
    checkout_order
)

app_name = 'v1_order'

urlpatterns = [
    path('edit_order', edit_or_create_order, name='edit'),
    path('my_orders', get_self_orders, name='self_orders'),
    path('view_order', view_order, name='view'),
    path('delete_order', delete_order, name='delete'),
    path('checkout', checkout_order, name='checkout')
]
