from django.urls import (include, path)
from . import views

urlpatterns = [
    path('ping', views.ping, name='ping'),
    # path('account/', include('v1_account.urls')),
    # path('machine/', include('v1_machine.urls')),
    # path('prod_hist/', include('v1_prod_hist.urls')),
    # path('order/', include('v1_order.urls')),
    # path('product/', include('v1_product.urls')),
]
