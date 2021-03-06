from django.urls import path
from .views import (get_all, search_by_filter, search_by_name)

app_name = 'v1_product'

urlpatterns = [
    path('all', get_all, name='all'),
    path('filter', search_by_filter, name='filter'),
    path('search', search_by_name, name='search'),
]
