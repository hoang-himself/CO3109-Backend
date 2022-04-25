from django.urls import path
from .views import (get_all_machine, clear_order, about_self, get_order_queue)

app_name = 'v1_machine'

urlpatterns = [
    path('all', get_all_machine),
    path('about', about_self, name='about'),
    path('order_queue', get_order_queue, name='order_queue'),
    path('clear_order', clear_order, name='clear_order')
]
