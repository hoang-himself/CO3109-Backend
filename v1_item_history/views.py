from django.contrib.auth import get_user_model
from rest_framework.decorators import (api_view, permission_classes)
from rest_framework.response import Response
from rest_framework import (permissions, status)

from mainframe.models import ItemHistory
from mainframe.serializers import (
    EnhancedModelSerializer, ItemHistorySerializer
)
from mainframe.utils import request_header_to_object
from mainframe.views import get_all_object

import datetime

CustomUser = get_user_model()


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_all(_):
    return get_all_object(ItemHistory, ItemHistorySerializer)


class SelfItemHistory(EnhancedModelSerializer):
    class Meta:
        model = ItemHistory
        fields = ('item', 'quantity', 'time')


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_history(request):
    user_obj = request_header_to_object(CustomUser, request)
    item_queryset = ItemHistory.objects.filter(user=user_obj)

    from_time = datetime.datetime.now() - datetime.timedelta(weeks=1)
    to_time = datetime.datetime.now()
    for (key, value) in request.GET.items():
        _key = key.lower()
        if not value:
            continue
        if _key == 'fromtime':
            from_time = datetime.datetime.fromtimestamp(int(value) / 1000)
        elif _key == 'totime':
            to_time = datetime.datetime.fromtimestamp(int(value) / 1000)

    return Response(
        status=status.HTTP_200_OK,
        data=SelfItemHistory(
            item_queryset.filter(time__range=(from_time, to_time)), many=True
        ).data
    )
