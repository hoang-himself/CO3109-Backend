from annoying.functions import get_object_or_None

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

from rest_framework import (exceptions, permissions, status)
from rest_framework.decorators import (api_view, permission_classes)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from mainframe.serializers import (
    EnhancedModelSerializer, CustomUserSerializer
)
from mainframe.views import (create_object, get_all_object)
from mainframe.utils import request_header_to_object

CustomUser = get_user_model()


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_all_account(_):
    return get_all_object(CustomUser, CustomUserSerializer)


class UserSelfSerializer(EnhancedModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'phone', 'credit']


class PasswdUserSerializer(EnhancedModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['password']


@api_view(['GET'])
def about_self(request):
    user_obj = request_header_to_object(CustomUser, request)
    return Response(UserSelfSerializer(user_obj).data)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def sign_up(request):
    norm_data = {}
    for key, value in request.data.items():
        norm_data[key] = value
    return create_object(CustomUser, data=norm_data)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def sign_in(request):
    valid = True
    errors = {}

    email = request.data.get('email', None)
    password = request.data.get('password', None)

    if not email:
        errors['email'] = 'This field is required'
        valid = False

    if not password:
        errors['password'] = 'This field is required'
        valid = False

    if (valid == False):
        raise exceptions.NotAuthenticated(errors)

    if ((user := get_object_or_None(CustomUser, email=email)) is None):
        raise exceptions.NotFound('User email not found')

    if not (user.is_active):
        raise exceptions.NotFound('User inactive')

    ser_user = PasswdUserSerializer(user).data
    if not check_password(password, ser_user.get('password', None)):
        raise exceptions.AuthenticationFailed('Wrong password')

    refresh_token = RefreshToken.for_user(user)
    access_token = refresh_token.access_token

    refresh_token = str(refresh_token)
    access_token = str(access_token)

    return Response(
        status=status.HTTP_200_OK, data={'access_token': access_token}
    )


@api_view(['DELETE'])
def sign_out(request):
    user_obj = request_header_to_object(CustomUser, request)
    if (user_obj is None):
        raise exceptions.NotFound('User not found')
    return Response(status=status.HTTP_200_OK, data=['Ok'])


@api_view(['PUT'])
@permission_classes([permissions.AllowAny])
def reset_credit(request):
    new_credit = request.data.get('new_credit', 3000)
    CustomUser.objects.all().update(credit=new_credit)
    return Response(status=status.HTTP_200_OK, data=['Ok'])
