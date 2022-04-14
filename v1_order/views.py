from django.contrib.auth import get_user_model

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import (exceptions, serializers, status)

from mainframe.models import (Order, Product)
from mainframe.serializers import EnhancedModelSerializer

CustomUser = get_user_model()


class ProductField(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('uuid', 'image', 'name', 'price')


class ImplicitOrder(EnhancedModelSerializer):
    item = ProductField()

    class Meta:
        model = Order
        fields = ('order_id', 'item', 'quantity')


@api_view(['POST'])
def add_item(request):
    # TODO If order_id is null then create new order, else edit
    pass


@api_view(['GET'])
def view_order(request):
    order_id = request.GET.get('order_id', None)
    if order_id is None:
        raise exceptions.ParseError('order_id is required')
    return Response(
        status=status.HTTP_200_OK,
        data=ImplicitOrder(Order.objects.filter(order_id=order_id),
                           many=True).data
    )


@api_view(['PUT'])
def set_item_quantity(request):
    # TODO Requires order_id, item uuid, quantity
    pass


@api_view(['DELETE'])
def delete_order(request):
    # TODO Requires order_id
    pass


@api_view(['POST'])
def checkout_order(request):
    # TODO Assign machine_id to known order_id
    pass
