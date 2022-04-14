from django.urls import path
from . import views

app_name = 'v1_product'

urlpatterns = [
    path('all', views.get_all, name='all'),
    path('filter', views.search_by_filter, name='filter'),
    path('search', views.search_by_name, name='search'),
]
