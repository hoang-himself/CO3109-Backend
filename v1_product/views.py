from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework.decorators import api_view

from mainframe.utils import get_by_uuid
from mainframe.views import (
    create_object, edit_object, delete_object, get_object, get_all_object
)
from mainframe.models import Product
from mainframe.serializers import ProductSerializer, EnhancedModelSerializer
from rest_framework import serializers

CustomUser = get_user_model()


class ImplicitProduct(EnhancedModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'image', 'price', 'uuid')


@api_view(['GET'])
def get_all(_):
    return get_all_object(Product, ImplicitProduct)


@api_view(['GET'])
def get_search(request):
    instances = Product.objects.filter(name__icontains=request.GET.get('key'))
    return Response(ImplicitProduct(instances, many=True).data)


@api_view(['GET'])
def get_filter(request):
    dic = {}
    for (key, value) in request.GET.items():
        query = key.lower()
        if query == 'brand':
            query += '__name__icontains'
        elif query == 'fromprice':
            query = 'price__gt'
        elif query == 'toprice':
            query = 'price__lt'
        else:
            query += "__icontains"
        dic.update({query: value})
    instances = Product.objects.filter(**dic)
    return Response(ImplicitProduct(instances, many=True).data)


@api_view(['GET'])
def get_popular(_):
    instances = Product.objects.order_by('?')[:6]
    return Response(ImplicitProduct(instances, many=True).data)


@api_view(['GET'])
def get_related(_):
    instances = Product.objects.order_by('?')[:5]
    return Response(ImplicitProduct(instances, many=True).data)
