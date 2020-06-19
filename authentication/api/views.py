from rest_framework.views import APIView
from .serializers import SignupSerializer
from rest_framework.permissions import AllowAny
from django.conf import settings
from rest_framework import serializers, exceptions
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework.response import Response

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

