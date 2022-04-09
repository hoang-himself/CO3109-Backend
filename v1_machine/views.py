from annoying.functions import get_object_or_None

from rest_framework import (exceptions, status)
from rest_framework.decorators import api_view
from rest_framework.response import Response

from mainframe.models import Machine
from mainframe.serializers import MachineSerializer
from mainframe.utils import request_header_to_object


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
def get_all(_):
    return Response(
        status=status.HTTP_200_OK,
        data=MachineSerializer(Machine.objects.all(), many=True).data
    )


@api_view(['GET'])
def about_self(request):
    machine = request_header_to_machine(request)
    return Response(
        status=status.HTTP_200_OK, data=MachineSerializer(machine).data
    )


# TODO
@api_view(['GET'])
def get_order_queue(request):
    return Response(
        status=status.HTTP_200_OK,
        data={
            'queue':
                [
                    {
                        'uuid': 'blah',
                        'name': 'Drink 1'
                    }, {
                        'uuid': 'bleh',
                        'name': 'Drink 2'
                    }
                ]
        }
    )
    machine_obj = request_header_to_object(request, Machine)
    machine = MachineSerializer(machine_obj).data
