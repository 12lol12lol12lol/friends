from typing import Any, Dict
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password, ]
    )
    password2 = serializers.CharField(
        write_only=True, required=True, validators=[validate_password, ]
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'password2')

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        data = super().validate(attrs)
        if data['password'] != data['password2']:
            raise serializers.ValidationError('Passwords do not match')
        return data

    def create(self, attrs: Dict[str, Any]) -> User:
        return User.objects.create_user(
            username=attrs['username'],
            password=attrs['password']
        )
