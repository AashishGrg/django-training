from django.conf import settings
from rest_framework import serializers
from django.core import validators


class SignupSerializer(serializers.Serializer):
    email = serializers.CharField()
    phone = serializers.CharField(max_length=10,
                                  validators=[validators.int_list_validator(), validators.MinLengthValidator(10)])
    password = serializers.CharField()
    user_type = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    class Meta:
        fields = ('first_name', 'last_name', 'email', 'phone', 'password', 'user_type',)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(style={'input_type': 'password'})


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_password(self, value):
        if len(value) < getattr(settings, 'PASSWORD_MIN_LENGTH', 8):
            raise serializers.ValidationError("Password should be atleast %s characters long." % getattr(
                settings, 'PASSWORD_MIN_LENGTH', 8)
                                              )
        return value

    def validate(self, data):
        if data.get('old_password') == data.get('new_password'):
            raise serializers.ValidationError({'detail': 'You have entered old password'})
        return data

    def validate_new_password(self, value):
        self.validate_password(value)
        return value
