from django.urls import (include, path)
from .views import ping

# This will change the pattern of reverse paths
#app_name = 'mainframe'

urlpatterns = [
    path('ping', ping, name='ping'),
    path('account/', include('v1_account.urls')),
    path('machine/', include('v1_machine.urls')),
    path('product/', include('v1_product.urls'))
    # path('prod_hist/', include('v1_prod_hist.urls')),
    # path('order/', include('v1_order.urls')),
]
