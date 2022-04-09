from django.urls import path
from .views import (about_self, sign_up, get_all, sign_in, sign_out)

app_name = 'v1_account'

urlpatterns = [
    path('signup', sign_up),
    path('signin', sign_in),
    path('me', about_self),
    path('signout', sign_out),
    path('all', get_all)
]
