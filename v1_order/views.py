from django.contrib.auth import get_user_model

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import (exceptions, serializers, status)

from mainframe.models import (Machine, Order, Product)
from mainframe.serializers import EnhancedModelSerializer
from mainframe.utils import request_header_to_object

CustomUser = get_user_model()


class ProductField(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('uuid', 'image', 'name', 'price')


class ImplicitOrder(EnhancedModelSerializer):
    class Meta:
        model = Order
        fields = ('order_uuid', 'machine')


class ExplicitOrder(EnhancedModelSerializer):
    item = ProductField()

    class Meta:
        model = Order
        fields = ('order_uuid', 'item', 'quantity', 'machine')


@api_view(['POST'])
def add_item_or_create_order(request):
    # TODO If order_uuid is null then create new order, else edit
    pass


@api_view(['GET'])
def get_self_orders(request):
    user_obj = request_header_to_object(request, CustomUser)
    return Response(
        status=status.HTTP_200_OK,
        data=ImplicitOrder(
            Order.objects.filter(user=user_obj).distinct('user'), many=True
        ).data
    )


@api_view(['GET'])
def view_order(request):
    order_uuid = request.GET.get('order_uuid', None)
    if order_uuid is None:
        raise exceptions.ParseError('order_uuid is required')
    return Response(
        status=status.HTTP_200_OK,
        data=ExplicitOrder(
            Order.objects.filter(order_uuid=order_uuid), many=True
        ).data
    )


@api_view(['PUT'])
def set_item_quantity(request):
    missing_field = {}
    if (order_uuid := request.data.get('order_uuid', None)) is None:
        missing_field.update({'order_uuid': 'This field is required.'})
    if (item_uuid := request.data.get('item_uuid', None)) is None:
        missing_field.update({'item_uuid': 'This field is required.'})
    if (new_quantity := request.data.get('new_quantity', None)) is None:
        missing_field.update({'new_quantity': 'This field is required.'})

    if bool(missing_field):
        raise exceptions.ParseError(missing_field)
    if (int(new_quantity) < 0):
        raise exceptions.ParseError(
            {'new_quantity': 'This field cannot be negative'}
        )

    order_obj = Order.objects.filter(
        order_uuid=order_uuid, item__uuid=item_uuid
    )
    if order_obj is None:
        raise exceptions.NotFound(['Order item not found'])

    order_obj.update(quantity=new_quantity)
    return Response(['ok'])


@api_view(['DELETE'])
def delete_order(request):
    if (order_uuid := request.data.get('order_uuid', None)) is None:
        raise exceptions.ParseError({'order_uuid': 'This field is required.'})
    Order.objects.filter(order_uuid=order_uuid).delete()
    return Response(status=status.HTTP_200_OK, data=['ok'])


@api_view(['PUT'])
def checkout_order(request):
    missing_field = {}
    if (order_uuid := request.data.get('order_uuid', None)) is None:
        missing_field.update({'order_uuid': 'This field is required.'})
    if (machine_uuid := request.data.get('machine_uuid', None)) is None:
        missing_field.update({'machine_uuid': 'This field is required.'})

    if bool(missing_field):
        raise exceptions.ParseError(missing_field)

    order_obj = Order.objects.filter(order_uuid=order_uuid)
    machine_obj = Machine.objects.get(uuid=machine_uuid)
    if order_obj is None:
        raise exceptions.NotFound(['Order item not found'])
    if machine_obj is None:
        raise exceptions.NotFound(['Machine not found'])

    order_obj.update(machine=machine_obj)
    return Response(['ok'])
