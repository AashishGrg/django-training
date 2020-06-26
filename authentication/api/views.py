from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.views import APIView
from .serializers import SignupSerializer, LoginSerializer, PasswordChangeSerializer, ProfileSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.conf import settings
from rest_framework import serializers, exceptions, status
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


class PasswordChangeAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PasswordChangeSerializer

    def get_object(self):
        obj = self.request.user
        return obj

    def post(self, request):
        self.object = self.get_object()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            if not self.object.check_password(serializer.data.get("old_password")):
                raise APIException("you entered wrong password")
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response({"success": "Password changed successfully."}, status=status.HTTP_200_OK)


# http://www.cdrf.co for documentation

class UserProfileAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get(self, request, *args, **kwargs):
        user_obj = request.user
        user_data = self.serializer_class(user_obj).data
        return Response(data=user_data, status=status.HTTP_200_OK)


class UserProfileUpdateAPIView(UpdateAPIView):
    queryset = PortalUser.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer

    def patch(self, request, *args, **kwargs):
        user_obj_id = self.kwargs['pk']
        if request.user.id == user_obj_id:
            return self.partial_update(request, *args, **kwargs)
        return Response({'detail': 'you dont have permission to update the profile'},
                        status=status.HTTP_400_BAD_REQUEST)
