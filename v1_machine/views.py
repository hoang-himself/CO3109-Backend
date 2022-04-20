from annoying.functions import get_object_or_None

from rest_framework.decorators import (api_view, permission_classes)
from rest_framework.response import Response
from rest_framework import (exceptions, serializers, permissions, status)

from mainframe.models import (Order, Product, Machine)
from mainframe.serializers import (EnhancedModelSerializer, MachineSerializer)


class InternalMachineSerializer(EnhancedModelSerializer):
    class Meta:
        model = Machine
        fields = '__all__'


class ProductField(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('uuid', 'image', 'name', 'price')


class ImplicitOrder(EnhancedModelSerializer):
    machine_uuid = serializers.CharField(source='machine.uuid')
    item = ProductField()

    class Meta:
        model = Order
        fields = ('machine_uuid', 'order_uuid', 'item', 'quantity')


def request_header_to_machine(request):
    uuid_header = request.headers.get('X-MACHINE-UUID', None)
    if (uuid_header is None):
        raise exceptions.AuthenticationFailed(
            {'X-MACHINE-UUID': 'This header is required.'}
        )
    uuid = uuid_header.split(' ')[1]
    obj = get_object_or_None(Machine, uuid=uuid)
    if (obj is None):
        raise exceptions.NotFound('Not found.')
    return obj


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def about_self(request):
    machine = request_header_to_machine(request)
    return Response(
        status=status.HTTP_200_OK, data=MachineSerializer(machine).data
    )


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_order_queue(request):
    machine_obj = request_header_to_machine(request)
    machine_data = InternalMachineSerializer(machine_obj).data
    return Response(
        status=status.HTTP_200_OK,
        data=ImplicitOrder(
            Order.objects.filter(machine=machine_data.get('id')
                                ).order_by('order_uuid'),
            many=True
        ).data
    )


@api_view(['DELETE'])
@permission_classes([permissions.AllowAny])
def clear_order(request):
    # TODO After machine successfully dispenses drinks, clear order from table
    # and add to prod_hist
    return Response(status=status.HTTP_200_OK, data=['ok'])
