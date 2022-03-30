from annoying.functions import get_object_or_None

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import (check_password, make_password)

from rest_framework import (exceptions, status)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from mainframe.views import (
    create_object, get_object, edit_object, delete_object
)
from mainframe.serializers import (
    EnhancedModelSerializer, CustomUserSerializer
)
from v1_order.views import request_to_user_object

CustomUser = get_user_model()


class UserSelfSerializer(EnhancedModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'email', 'first_name',
            'last_name', 'phone'
        ]


class UserSelfView(APIView):
    def get(self, request):
        user = request_to_user_object(request)
        return Response(UserSelfSerializer(user).data)


class UserView(APIView):
    def post(self, request):
        norm_data = {}
        for key, value in request.data.items():
            norm_data[key] = value
        return create_object(CustomUser, data=norm_data)

    def get(self, _):
        return Response(
            CustomUserSerializer(CustomUser.objects.all(), many=True).data
        )

    # def patch(self, request):
    #     return edit_object(CustomUser, data=request.data)

    # def delete(self, request):
    #     return delete_object(CustomUser, data=request.data)


class PasswdUserSerializer(EnhancedModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['password']


class AuthView(APIView):
    def post(self, request):
        valid = True
        errors = {}

        email = request.data.get('email', None)
        password = request.data.get('password', None)

        if not email:
            errors['email'] = 'This field is required.'
            valid = False

        if not password:
            errors['password'] = 'This field is required.'
            valid = False

        if (valid == False):
            raise exceptions.NotAuthenticated(errors)

        if ((user := get_object_or_None(CustomUser, email=email)) is None):
            raise exceptions.NotFound('User email not found.')

        if not (user.is_active):
            raise exceptions.NotFound('User inactive.')

        ser_user = PasswdUserSerializer(user).data
        if not check_password(password, ser_user.get('password', None)):
            raise exceptions.AuthenticationFailed('Wrong password.')

        refresh_token = RefreshToken.for_user(user)
        access_token = refresh_token.access_token

        refresh_token = str(refresh_token)
        access_token = str(access_token)

        return Response(
            status=status.HTTP_200_OK,
            data={
                'access_token': access_token
            }
        )

    def delete(self, request):
        token = request.COOKIES.get('accesstoken', None)

        response = Response()
        if (token):
            response.delete_cookie('accesstoken')

        response.status_code = status.HTTP_200_OK
        response.data = {
            'detail': 'ok'
        }
        return response
