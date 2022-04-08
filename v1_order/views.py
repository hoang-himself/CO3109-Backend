from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view

from rest_framework import (exceptions, serializers, status)
from rest_framework.response import Response
from rest_framework.views import APIView

from mainframe.models import Order, Product
from mainframe.views import request_header_to_object
from mainframe.serializers import EnhancedModelSerializer

CustomUser = get_user_model()


class ProductField(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('uuid', 'image', 'name', 'price')


class ImplicitOrder(EnhancedModelSerializer):
    item = ProductField()

    class Meta:
        model = Order
        fields = ('item', 'quantity', 'order_id')


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

        user = request_header_to_object(request, CustomUser)
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
        user = request_header_to_object(request, CustomUser)
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

        user = request_header_to_object(request, CustomUser)
        item = Product.objects.get(uuid=uuid)

        obj = Order.objects.get(
            user=user,
            item=item,
        )
        obj.delete()
        return Response('Deleted')


@api_view(['POST'])
def assign_order_to_machine(request):
    pass

class UserCheckout(APIView):
    # Assign order to machine
    def post(self, request):
        # TODO Add machine_id to all orders
        order_id = request.data.get('order_id', None)
        user = request_header_to_object(request, CustomUser)
        user.Order.clear()
        return Response('Cleared')

    # Get orders of machine
    def get(self, request):
        machine_id = request.GET.get('machine_id', None)
        return Response(
            ImplicitOrder(
                Order.objects.filter(item__machine_id=machine_id), many=True
            ).data
        )

    # Here, machine will check if it has sufficient stock

    # Sufficient stock, mark order as paid then release drink
    def delete(self, request):
        # TODO delete items by order_id
        order_id = request.GET.get('order_id', None)
        return Response(status=status.HTTP_200_OK, data={})
