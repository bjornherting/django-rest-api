"""
Serializer for the user api view
"""
from rest_framework import serializers

from django.contrib.auth import (
    get_user_model,
    authenticate
)
from rest_framework.exceptions import   NotAuthenticated


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user model"""

    class Meta:
        model = get_user_model()
        fields = [
            'email',
            'password',
            'name'
        ]
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 5
            }
        }

    def create(self, validated_data):
        """Create a new user with encrypted password"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update and return user"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for auth token"""
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """"validate token"""
        email = attrs.get('email')
        password = attrs.get("password")
        if not email or password is None:
            raise serializers.ValidationError()

        user = authenticate(
            self.context.get('request'),
            username=email,
            password=password,
        )
        if not user:
            raise NotAuthenticated()

        attrs['user'] = user
        return attrs
