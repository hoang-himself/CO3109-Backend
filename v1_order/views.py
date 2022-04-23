from django.contrib.auth import get_user_model

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import (exceptions, serializers, status)

from uuid import uuid4

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


class OrderDetail(EnhancedModelSerializer):
    item = ProductField()

    class Meta:
        model = Order
        fields = ('item', 'quantity')


@api_view(['PUT'])
def edit_or_create_order(request):
    missing_field = {}
    order_uuid = request.data.get('order_uuid', None)
    if (item_uuid := request.data.get('item_uuid', None)) is None:
        missing_field.update({'item_uuid': 'This field is required'})
    if (quantity := request.data.get('quantity', None)) is None:
        missing_field.update({'quantity': 'This field is required'})
    if bool(missing_field):
        raise exceptions.ParseError(missing_field)

    # Delete item
    if (int(quantity) < 1):
        Order.objects.filter(
            order_uuid=order_uuid, is_paid=False, item__uuid=item_uuid
        ).delete()
        return Response(status=status.HTTP_200_OK, data=['Deleted'])

    user_obj = request_header_to_object(CustomUser, request)

    # New order
    order_queryset = Order.objects.filter(order_uuid=order_uuid)
    if not order_queryset.exists():
        order_uuid = uuid4()
        Order.objects.create(
            user=user_obj,
            order_uuid=order_uuid,
            item=Product.objects.get(uuid=item_uuid),
            quantity=quantity
        )
        return Response(
            status=status.HTTP_201_CREATED, data={'order_uuid': order_uuid}
        )

    # Order does not contain item
    order_queryset = order_queryset.filter(item__uuid=item_uuid)
    if not order_queryset.exists():
        Order.objects.create(
            user=user_obj,
            order_uuid=order_uuid,
            item=Product.objects.get(uuid=item_uuid),
            quantity=quantity
        )
        return Response(status=status.HTTP_200_OK, data=['Ok'])

    # Just update quantity
    order_queryset.update(quantity=quantity)
    return Response(status=status.HTTP_200_OK, data=['Ok'])


@api_view(['GET'])
def get_orders(request):
    user_obj = request_header_to_object(CustomUser, request)

    order_queryset = Order.objects.filter(user=user_obj)
    dic = {'is_paid': False}
    for key, value in request.GET.items():
        _key = key.lower()
        _value = value.lower()
        if not _key == 'history':
            continue

        if _value == 'paid':
            dic.update({'is_paid': True})
        elif _value == 'all':
            dic.pop('is_paid')
        else:
            dic.update({'is_paid': False})

    return Response(
        status=status.HTTP_200_OK,
        data=ImplicitOrder(
            order_queryset.filter(**dic).distinct('order_uuid'), many=True
        ).data
    )


@api_view(['GET'])
def view_order(request):
    order_uuid = request.GET.get('order_uuid', None)
    if order_uuid is None:
        raise exceptions.ParseError('order_uuid is required')
    return Response(
        status=status.HTTP_200_OK,
        data=OrderDetail(
            Order.objects.filter(order_uuid=order_uuid), many=True
        ).data
    )


@api_view(['DELETE'])
def delete_order(request):
    if (order_uuid := request.data.get('order_uuid', None)) is None:
        raise exceptions.ParseError({'order_uuid': 'This field is required'})
    Order.objects.filter(order_uuid=order_uuid, is_paid=False).delete()
    return Response(status=status.HTTP_200_OK, data=['Deleted'])


class MinimalProductField(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('uuid', 'price')


class MinimalOrderSerializer(EnhancedModelSerializer):
    item = MinimalProductField()

    class Meta:
        model = Order
        fields = ('item', 'quantity')


@api_view(['PUT'])
def checkout_order(request):
    missing_field = {}
    if (order_uuid := request.data.get('order_uuid', None)) is None:
        missing_field.update({'order_uuid': 'This field is required'})
    if (machine_uuid := request.data.get('machine_uuid', None)) is None:
        missing_field.update({'machine_uuid': 'This field is required'})

    if bool(missing_field):
        raise exceptions.ParseError(missing_field)

    order_queryset = Order.objects.filter(order_uuid=order_uuid, is_paid=False)
    machine_obj = Machine.objects.get(uuid=machine_uuid)
    if order_queryset is None:
        raise exceptions.NotFound(['Order item not found'])
    if machine_obj is None:
        raise exceptions.NotFound(['Machine not found'])

    order_data = MinimalOrderSerializer(order_queryset, many=True).data
    user_obj = order_queryset.first().user

    total_price = 0
    for order in order_data:
        total_price += order.get('item').get('price') * order.get('quantity')
    if total_price > user_obj.credit:
        raise exceptions.ValidationError(['Insufficient credits'])

    user_obj.credit -= total_price
    user_obj.save()

    order_queryset.update(machine=machine_obj, is_paid=True)
    return Response(status=status.HTTP_202_ACCEPTED, data=['Ok'])
