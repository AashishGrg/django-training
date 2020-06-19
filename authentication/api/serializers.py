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
