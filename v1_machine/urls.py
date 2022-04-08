from django.urls import path
from .views import (get_all, about_self)

app_name = 'v1_brand'

urlpatterns = [
    path('all', get_all),
    path('about', about_self),
]
