from django.urls import path
from .views import (get_all, get_one, get_current)

app_name = 'v1_brand'

urlpatterns = [
    path('all', get_all),
    path('about', get_one),
]
