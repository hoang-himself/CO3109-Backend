from django.contrib.auth import get_user_model

from rest_framework.decorators import (api_view, permission_classes)
from rest_framework.response import Response
from rest_framework import (permissions, status)

from mainframe.models import Product
from mainframe.views import get_all_object
from mainframe.serializers import EnhancedModelSerializer

CustomUser = get_user_model()


class ImplicitProduct(EnhancedModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'unit', 'image', 'price', 'uuid')


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_all_product(_):
    return get_all_object(Product, ImplicitProduct)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def search_by_name(request):
    item_queryset = Product.objects.filter(name__icontains=request.GET.get('key'))
    return Response(
        status=status.HTTP_200_OK,
        data=ImplicitProduct(item_queryset, many=True).data
    )


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
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
    item_queryset = Product.objects.filter(**dic)
    return Response(
        status=status.HTTP_200_OK,
        data=ImplicitProduct(item_queryset, many=True).data
    )
