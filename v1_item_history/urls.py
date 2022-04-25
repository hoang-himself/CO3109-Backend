from django.urls import path
from .views import (get_all, get_history)

app_name = 'v1_item_history'

urlpatterns = [path('all', get_all), path('my', get_history, name='history')]
