from django.urls import path
from .views import (
    add_item, view_order, set_item_quantity, delete_order, checkout_order
)

app_name = 'v1_order'

urlpatterns = [
    path('add_item', add_item, name='add'),
    path('view_order', view_order, name='view'),
    path('item_quantity', set_item_quantity, name='item_quantity'),
    path('delete_order', delete_order, name='delete'),
    path('checkout', checkout_order, name='checkout')
]
