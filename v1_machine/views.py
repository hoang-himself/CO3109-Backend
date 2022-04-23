from annoying.functions import get_object_or_None

from rest_framework.decorators import (api_view, permission_classes)
from rest_framework.response import Response
from rest_framework import (exceptions, serializers, permissions, status)

from mainframe.models import (Order, Product, Machine)
from mainframe.serializers import (EnhancedModelSerializer, MachineSerializer)


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
def about_self(request):
    machine = request_header_to_machine(request)
    return Response(
        status=status.HTTP_200_OK, data=MachineSerializer(machine).data
    )


class InternalMachineSerializer(EnhancedModelSerializer):
    class Meta:
        model = Machine
        fields = '__all__'


class ProductField(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('uuid', 'image', 'name', 'price')


class ImplicitOrderSerializer(EnhancedModelSerializer):
    machine_uuid = serializers.CharField(source='machine.uuid')
    item = ProductField()

    class Meta:
        model = Order
        fields = ('machine_uuid', 'order_uuid', 'item', 'quantity')


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_order_queue(request):
    machine_obj = request_header_to_machine(request)
    machine_data = InternalMachineSerializer(machine_obj).data
    return Response(
        status=status.HTTP_200_OK,
        data=ImplicitOrderSerializer(
            Order.objects.filter(machine=machine_data.get('id'),
                                 is_paid=False).order_by('order_uuid'),
            many=True
        ).data
    )


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def clear_order(request):
    if (order_uuid := request.data.get('order_uuid', None)) is None:
        raise exceptions.ParseError({'order_uuid': 'This field is required'})

    order_queryset = Order.objects.filter(order_uuid=order_uuid, is_paid=False)
    if not order_queryset.exists():
        raise exceptions.NotFound({'order_uuid': 'Order not found'})

    # We can add an is_dispensed field here, but I'm lazy
    return Response(status=status.HTTP_200_OK, data=['Ok'])
