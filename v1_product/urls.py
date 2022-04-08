from django.urls import path
from . import views

app_name = 'v1_product'

urlpatterns = [
    path('all', views.get_all, name='product_all'),
    # path('popular', views.get_popular, name='product_popular'),
    # path('related', views.get_related, name='product_related'),
    path('filter', views.search_by_filter, name='product_filter'),
    path('search', views.search_by_name, name='product_search'),
]
