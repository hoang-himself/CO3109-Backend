from django.contrib.auth import get_user_model

from rest_framework.decorators import api_view
from rest_framework.response import Response

from mainframe.models import Product
from mainframe.views import get_all_object
from mainframe.serializers import EnhancedModelSerializer

CustomUser = get_user_model()


class ImplicitProduct(EnhancedModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'unit', 'image', 'price', 'uuid')


@api_view(['GET'])
def get_all(_):
    return get_all_object(Product, ImplicitProduct)


@api_view(['GET'])
def search_by_name(request):
    instances = Product.objects.filter(name__icontains=request.GET.get('key'))
    return Response(ImplicitProduct(instances, many=True).data)


@api_view(['GET'])
def search_by_filter(request):
    dic = {}
    for (key, value) in request.GET.items():
        query = key.lower()
        if query == 'fromprice':
            query = 'price__gt'
        elif query == 'toprice':
            query = 'price__lt'
        else:
            query += "__icontains"
        dic.update({query: value})
    instances = Product.objects.filter(**dic)
    return Response(ImplicitProduct(instances, many=True).data)
