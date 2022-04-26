from django.urls import path
from .views import (
    get_all, complete_order, about_self, get_order_queue, get_next_order
)

app_name = 'v1_machine'

urlpatterns = [
    path('all', get_all),
    path('about', about_self, name='about'),
    path('order_queue', get_order_queue, name='order_queue'),
    path('next_order', get_next_order, name='next_order'),
    path('complete_order', complete_order, name='complete_order')
]
