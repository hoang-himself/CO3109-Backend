from annoying.functions import get_object_or_None
from django.contrib.auth import get_user_model
from django.db import models

from rest_framework import (exceptions, permissions, status)
from rest_framework.decorators import (api_view, permission_classes)
from rest_framework.response import Response
from rest_framework import serializers

from mainframe.models import (Machine, Order, OrderItem, OrderQueue, Product)
from mainframe.serializers import (EnhancedModelSerializer, OrderSerializer)
from mainframe.utils import request_header_to_object
from mainframe.views import get_all_object

CustomUser = get_user_model()


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_all(_):
    return get_all_object(Order, OrderSerializer)


@api_view(['PUT'])
def edit_or_create_order(request):
    missing_field = {}
    uuid = request.data.get('uuid', None)
    create = uuid is None
    if (name := request.data.get('name', None)) is None:
        missing_field.update({'name': 'This field is required'})
    if (item_uuid := request.data.get('item_uuid', None)) is None:
        missing_field.update({'item_uuid': 'This field is required'})
    if (quantity := request.data.get('quantity', None)) is None:
        missing_field.update({'quantity': 'This field is required'})
    if bool(missing_field):
        raise exceptions.ParseError(missing_field)

    uuid_list = item_uuid.replace(' ', '').split(',')
    quantity_list = quantity.replace(' ', '').split(',')
    if len(uuid_list) != len(quantity_list):
        raise exceptions.ParseError(
            {
                'quantity':
                    'The length of quantity must be the same as item_uuid'
            }
        )
    user_obj = request_header_to_object(CustomUser, request)

    ### New order
    item_obj = [get_object_or_None(Product, uuid=i) for i in uuid_list]
    if (any(i is None for i in item_obj)):
        raise exceptions.ParseError({'item_uuid': 'Invalid item_uuid'})

    if create:
        new_order = Order.objects.create(
            user=user_obj,
            name=name,
        )
        OrderItem.objects.bulk_create(
            [
                OrderItem(order=new_order, item=i, quantity=q)
                for i, q in zip(item_obj, quantity_list)
            ]
        )
    else:  # Edit order
        if (order_obj := get_object_or_None(Order, uuid=uuid)) is None:
            raise exceptions.ParseError({'uuid': 'Invalid uuid'})
        for i, q in zip(item_obj, quantity_list):
            q = int(q)
            if orderItem := get_object_or_None(
                OrderItem, order=order_obj, item=i
            ):
                if q < 1:  # Delete item
                    orderItem.delete()
                else:  # Set quantity
                    orderItem.quantity = q
                    orderItem.save()
            else:
                if q < 1:
                    raise exceptions.ParseError(
                        {
                            'quantity':
                                'Cannot create an order with quantity < 1'
                        }
                    )
                OrderItem.objects.create(order=order_obj, item=i, quantity=q)

    return Response(status=status.HTTP_200_OK, data=['Ok'])


class SimpleRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        return value


class SimpleImageField(serializers.RelatedField):
    def to_representation(self, value):
        return '/media' + value


class ImplicitOrder(EnhancedModelSerializer):
    total_price = SimpleRelatedField(read_only=True)
    image = SimpleImageField(read_only=True)

    class Meta:
        model = Order
        fields = ('uuid', 'name', 'total_price', 'image')


@api_view(['GET'])
def get_orders(request):
    user_obj = request_header_to_object(CustomUser, request)
    order_queryset = Order.objects.filter(user=user_obj).annotate(
        total_price=models.Sum(
            models.F('order_item_set__item__price') * models.F('order_item_set__quantity'),
            output_field=models.FloatField()
        )
    ).annotate(
        image=models.Min('order_item_set__item__image',
            output_field=models.ImageField()
        )
    )

    return Response(
        status=status.HTTP_200_OK,
        data=ImplicitOrder(order_queryset, many=True).data
    )


class ProductDetail(EnhancedModelSerializer):
    class Meta:
        model = Product
        fields = ('uuid', 'image', 'name', 'price')


class OrderItemDetail(EnhancedModelSerializer):
    item = ProductDetail()

    class Meta:
        model = OrderItem
        fields = ('item', 'quantity')


class OrderDetail(EnhancedModelSerializer):
    order_item_set = OrderItemDetail(many=True)

    class Meta:
        model = Order
        fields = ('name', 'order_item_set')


@api_view(['GET'])
def view_order(request):
    uuid = request.GET.get('uuid', None)
    if uuid is None:
        raise exceptions.ParseError({'uuid': 'This field is required'})

    return Response(
        status=status.HTTP_200_OK,
        data=OrderDetail(Order.objects.get(uuid=uuid)).data
    )


@api_view(['DELETE'])
def delete_order(request):
    if (uuid := request.data.get('uuid', None)) is None:
        raise exceptions.ParseError({'uuid': 'This field is required'})
    if order := get_object_or_None(Order, uuid=uuid):
        order.delete()
    else:
        raise exceptions.ParseError({'uuid': 'Invalid uuid'})
    return Response(status=status.HTTP_200_OK, data=['Deleted'])


class ProductShort(EnhancedModelSerializer):
    class Meta:
        model = Product
        fields = ('price', )


class OrderItemShort(EnhancedModelSerializer):
    item = ProductShort()

    class Meta:
        model = OrderItem
        fields = ('item', 'quantity')


class OrderShort(EnhancedModelSerializer):
    order_item_set = OrderItemShort(many=True)

    class Meta:
        model = Order
        fields = ('order_item_set', )


@api_view(['PUT'])
def checkout_order(request):
    if (order_uuid := request.data.get('order_uuid', None)) is None:
        raise exceptions.ParseError({'order_uuid': 'This field is required'})
    if (machine_uuid := request.data.get('machine_uuid', None)) is None:
        raise exceptions.ParseError({'machine_uuid': 'This field is required'})

    order_obj = Order.objects.get(uuid=order_uuid)
    machine_obj = Machine.objects.get(uuid=machine_uuid)
    if not order_obj:
        raise exceptions.NotFound(['Order item not found'])
    if not machine_obj:
        raise exceptions.NotFound(['Machine not found'])

    user_obj = order_obj.user
    order_data = OrderShort(order_obj).data.get('order_item_set', None)

    total_price = 0
    for order in order_data:
        total_price += order.get('item').get('price') * order.get('quantity')
    if total_price > user_obj.credit:
        raise exceptions.ValidationError(['Insufficient credits'])

    user_obj.credit -= total_price
    user_obj.save()

    OrderQueue.objects.create(order=order_obj, machine=machine_obj)
    return Response(status=status.HTTP_201_CREATED, data=['Ok'])
