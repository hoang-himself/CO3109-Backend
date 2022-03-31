from annoying.functions import get_object_or_None

from django.conf import settings
from django.contrib.auth import get_user_model

from rest_framework import (exceptions, fields, serializers, status)
from rest_framework.response import Response
# from rest_framework.response import Response
from rest_framework.views import APIView

from mainframe.views import (
    create_object, edit_object, get_object, delete_object
)
from mainframe.models import Order, Product
# from mainframe.serializers import OrderSerializer

import jwt

from mainframe.serializers import CustomUserSerializer, EnhancedModelSerializer, ProductSerializer

CustomUser = get_user_model()


class ProductField(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('uuid', 'image', 'name', 'price')


class ImplicitOrder(EnhancedModelSerializer):
    item = ProductField()

    class Meta:
        model = Order
        fields = ('item', 'quantity')


def request_to_user_object(request):
    token_header = request.headers.get('Authorization', None)
    token = token_header.split(' ')[1]

    if not (token):
        raise exceptions.AuthenticationFailed(
            {'access_token': 'This field is required.'}
        )

    try:
        payload = jwt.decode(token, settings.JWT_KEY, algorithms=['HS256'])
        if payload.get('typ', None) != 'access':
            raise exceptions.ParseError('Invalid access token.')
    except jwt.ExpiredSignatureError:
        raise exceptions.AuthenticationFailed('Access token expired.')

    if (
        (
            user :=
            get_object_or_None(CustomUser, uuid=payload.get('uuid', None))
        ) is None
    ):
        raise exceptions.NotFound('User not found.')
    return user


class UserCheckout(APIView):
    def delete(self, request):
        user = request_to_user_object(request)
        user.Order.clear()
        return Response('Cleared')


class UserOrderView(APIView):
    def put(self, request):
        catchError = {}
        if (uuid := request.data.get('uuid', None)) is None:
            catchError.update({'uuid': 'This field is required.'})
        if (quantity := request.data.get('quantity', None)) is None:
            catchError.update({'quantity': 'This field is required.'})

        if bool(catchError):
            raise exceptions.ParseError(catchError)
        elif quantity != 'add' and quantity <= 0:
            raise exceptions.ParseError(
                {'quantity': 'This field must be greater than 0'}
            )

        user = request_to_user_object(request)
        item = Product.objects.get(uuid=uuid)

        if item.price < 0:
            raise exceptions.ParseError(
                {'item': 'This product cannot be added to Order.'}
            )

        obj, created = Order.objects.get_or_create(
            user=user, item=item, defaults={"quantity": 1}
        )

        if quantity == 'add':
            obj.quantity = 1 if created else obj.quantity + 1
        else:
            obj.quantity = quantity

        obj.save()
        return Response('Ok')

    def post(self, request):
        user = request_to_user_object(request)
        return Response(
            ImplicitOrder(
                Order.objects.filter(user=user).order_by('item__name'),
                many=True
            ).data
        )

    def delete(self, request):
        catchError = {}
        if (uuid := request.data.get('uuid', None)) is None:
            catchError.update({'uuid': 'This field is required.'})

        if bool(catchError):
            raise exceptions.ParseError(catchError)

        user = request_to_user_object(request)
        item = Product.objects.get(uuid=uuid)

        obj = Order.objects.get(
            user=user,
            item=item,
        )
        obj.delete()
        return Response('Deleted')
