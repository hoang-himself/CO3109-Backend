from django.urls import path
from .views import (about_self, sign_up, sign_in, sign_out, reset_credit)

app_name = 'v1_account'

urlpatterns = [
    path('signup', sign_up, name='sign_up'),
    path('signin', sign_in, name='sign_in'),
    path('about', about_self, name='about'),
    path('signout', sign_out, name='sign_out'),
    path('this_should_be_run_with_cron_but_you_can_call_it_remotely_too', reset_credit, name='reset_credit')
]
