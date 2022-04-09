from django.urls import path
from .views import (get_all, about_self, get_order_queue)

app_name = 'v1_machine'

urlpatterns = [
    path('all', get_all, name='all'),
    path('about', about_self, name='about'),
    path('order_queue', get_order_queue, name='order_queue')
]
