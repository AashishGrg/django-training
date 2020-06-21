from rest_framework.views import APIView
from .serializers import SignupSerializer, LoginSerializer
from rest_framework.permissions import AllowAny
from django.conf import settings
from rest_framework import serializers, exceptions
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import NotFound, APIException

PortalUser = get_user_model()


# from django.core.exceptions import ValidationError

class SignupAPIView(APIView):
    permission_classes = (AllowAny,)

    def validate_password(self, value):
        if len(value) < getattr(settings, 'PASSWORD_MIN_LENGTH', 8):
            raise serializers.ValidationError("Password should be atleast %s characters long." % getattr(
                settings, 'PASSWORD_MIN_LENGTH', 8)
                                              )
        return value

    def post(self, request, *args, **kwargs):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data['email']
            phone = serializer.validated_data['phone']
            first_name = serializer.validated_data['first_name']
            last_name = serializer.validated_data['last_name']
            password = serializer.validated_data['password']
            user_type = serializer.validated_data['user_type']
            try:
                self.validate_password(password)
            except ValidationError as error:
                raise exceptions.ValidationError(error)
            user = PortalUser.objects.create(first_name=first_name, last_name=last_name, phone=phone, email=email,
                                             user_type=user_type)
            user.set_password(password)
            user.save()
            return Response({'data': serializer.data, 'success': 'User Registered Succesfully.'})


def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }


class LoginAPIView(APIView):
    def authenticate(self, request, email, password, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            raise NotFound("User with the provided email does not exist")
        else:
            if user.is_active:
                if user.check_password(password):
                    return user
                else:
                    raise APIException("Password Incorrect")
            raise NotFound("User is not activated.")

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user_obj = self.authenticate(request, email, password)
            if user_obj:
                token = get_token_for_user(user_obj)
                token['user_type'] = user_obj.user_type
                return Response(token)
            else:
                return Response({'detail': 'Active User not Found.'})