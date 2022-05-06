from annoying.functions import get_object_or_None

from django.conf import settings
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers

from rest_framework.decorators import (api_view, permission_classes)
from rest_framework.response import Response
from rest_framework import (exceptions, permissions, status)

from mainframe.models import (
    Machine, ItemHistory, Order, OrderItem, OrderQueue, Product
)
from mainframe.serializers import (EnhancedModelSerializer, MachineSerializer)
from mainframe.views import get_all_object


def request_header_to_machine(request):
    uuid_header = request.headers.get('X-MACHINE-UUID', None)
    if (uuid_header is None):
        raise exceptions.AuthenticationFailed(
            {'X-MACHINE-UUID': 'This header is required'}
        )
    uuid = uuid_header.split(' ')[1]
    obj = get_object_or_None(Machine, uuid=uuid)
    if (obj is None):
        raise exceptions.NotFound('Not found')
    return obj


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_all(_):
    return get_all_object(Machine, MachineSerializer)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def about_self(request):
    machine = request_header_to_machine(request)
    return Response(
        status=status.HTTP_200_OK, data=MachineSerializer(machine).data
    )


class ProductShort(EnhancedModelSerializer):
    class Meta:
        model = Product
        fields = ('uuid', 'name')


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


class OrderQueueShort(EnhancedModelSerializer):
    order = OrderShort()

    class Meta:
        model = OrderQueue
        fields = ('uuid', 'order')


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
@cache_page(settings.CACHE_TTL)
@vary_on_headers('X-MACHINE-UUID')
def get_order_queue(request):
    machine_obj = request_header_to_machine(request)
    order_queue_queryset = OrderQueue.objects.filter(machine=machine_obj)
    if not order_queue_queryset.exists():
        ret_stat = status.HTTP_204_NO_CONTENT
    else:
        ret_stat = status.HTTP_200_OK

    return Response(
        status=ret_stat,
        data=OrderQueueShort(order_queue_queryset, many=True).data
    )


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_next_order(request):
    machine_obj = request_header_to_machine(request)
    order_queue_queryset = OrderQueue.objects.filter(machine=machine_obj)
    if not order_queue_queryset.exists():
        ret_stat = status.HTTP_204_NO_CONTENT
    else:
        ret_stat = status.HTTP_200_OK

    return Response(
        status=ret_stat,
        data=OrderQueueShort(order_queue_queryset.first()).data
    )


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def invalidate_order(request):
    if (order_uuid := request.data.get('order_uuid', None)) is None:
        raise exceptions.ParseError({'order_uuid': 'This field is required'})

    order_queue_obj = get_object_or_None(OrderQueue, uuid=order_uuid)
    if not order_queue_obj:
        raise exceptions.NotFound({'order_uuid': 'Order not found'})

    order_queue_obj.delete()
    return Response(status=status.HTTP_200_OK, data=['Ok'])


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def complete_order(request):
    if (order_uuid := request.data.get('order_uuid', None)) is None:
        raise exceptions.ParseError({'order_uuid': 'This field is required'})

    order_queue_obj = get_object_or_None(OrderQueue, uuid=order_uuid)
    if not order_queue_obj:
        raise exceptions.NotFound({'order_uuid': 'Order not found'})

    user_obj = order_queue_obj.order.user
    item_queryset = order_queue_obj.order.order_item_set.all()

    ItemHistory.objects.bulk_create(
        [
            ItemHistory(user=user_obj, item=i.item, quantity=i.quantity)
            for i in item_queryset
        ]
    )

    order_queue_obj.delete()
    return Response(status=status.HTTP_200_OK, data=['Ok'])
