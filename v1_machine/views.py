from rest_framework.decorators import api_view

from mainframe.models import Machine
from mainframe.serializers import MachineSerializer
from mainframe.utils import request_header_to_object
from mainframe.views import (get_object, get_all_object)


@api_view(['GET'])
def get_all(_):
    return get_all_object(Machine)


@api_view(['GET'])
def about_self(request):
    return get_object(Machine, data=request.data)


# TODO
@api_view(['GET'])
def get_order_queue(request):
    machine_obj = request_header_to_object(request, Machine)
    machine = MachineSerializer(machine_obj).data
