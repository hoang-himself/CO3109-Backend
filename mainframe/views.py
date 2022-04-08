from django.contrib.auth import get_user_model

from rest_framework import (exceptions, status)
from rest_framework.decorators import (api_view, permission_classes)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .utils import (get_by_uuid, convert_primitive)
from . import models
from . import serializers

CustomUser = get_user_model()

SERIALIZERS = {
    models.ProductHistory: serializers.ProductHistorySerializer,
    models.Order: serializers.OrderSerializer,
    models.Product: serializers.ProductSerializer,
    CustomUser: serializers.CustomUserSerializer,
}

CREATE_RESPONSE = {'data': 'Ok', 'status': status.HTTP_201_CREATED}

EDIT_RESPONSE = {'data': 'Ok', 'status': status.HTTP_200_OK}

DELETE_RESPONSE = {'data': 'Deleted', 'status': status.HTTP_200_OK}

GET_RESPONSE = {'status': status.HTTP_200_OK}

LIST_RESPONSE = {'status': status.HTTP_200_OK}


def create_object(model, **kwargs):
    try:
        data = kwargs.pop('data')
    except KeyError:
        raise KeyError('Payload cannot be empty')
    Serializer = SERIALIZERS[model]
    serializer = Serializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(**CREATE_RESPONSE)
    else:
        raise exceptions.ParseError(convert_primitive(serializer.errors))


def edit_object(model, **kwargs):
    try:
        data = kwargs.pop('data').copy()
    except KeyError:
        raise KeyError('Payload cannot be empty')
    Serializer = SERIALIZERS[model]
    uuid = uuid[0] if isinstance(
        uuid := data.pop('uuid', None), list) else uuid
    instance = get_by_uuid(model, uuid)
    serializer = Serializer(instance=instance, data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(**EDIT_RESPONSE)
    else:
        raise exceptions.ParseError(convert_primitive(serializer.errors))


def get_object(model, explicit=None, **kwargs):
    try:
        data = kwargs.pop('data')
    except KeyError:
        raise KeyError('Payload cannot be empty')
    try:
        uuid = data['uuid']
    except KeyError:
        raise exceptions.ParseError({'uuid': 'This field is required.'})
    Serializer = SERIALIZERS[model] if explicit is None else explicit
    return Response(Serializer(get_by_uuid(model, uuid)).data)


def get_all_object(model, implicit=None):
    Serializer = SERIALIZERS[model] if implicit is None else implicit
    return Response(Serializer(model.objects.all(), many=True).data)


def delete_object(model, **kwargs):
    try:
        data = kwargs.pop('data')
    except KeyError:
        raise KeyError('Payload cannot be empty')
    try:
        uuid = data['uuid']
    except KeyError:
        raise exceptions.ParseError({'uuid': 'This field is required.'})
    get_by_uuid(model, uuid).delete()
    return Response(**DELETE_RESPONSE)


@api_view(['POST', 'GET', 'PATCH', 'DELETE'])
@permission_classes([AllowAny])
def ping(_):
    return Response(data={'detail': 'pong'}, status=status.HTTP_200_OK)
