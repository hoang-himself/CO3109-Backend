from django.urls import path
from .views import (
    get_all, complete_order, about_self, get_order_queue, get_next_order,
    invalidate_order
)

app_name = 'v1_machine'

urlpatterns = [
    path('all', get_all),
    path('about', about_self, name='about'),
    path('queue', get_order_queue, name='queue'),
    path('next', get_next_order, name='next'),
    path('invalidate', invalidate_order, name='invalidate'),
    path('complete', complete_order, name='complete')
]
