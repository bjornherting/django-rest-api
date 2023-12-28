"""
Serializer for the user api view
"""

from rest_framework import serializers

from django.contrib.auth import get_user_model


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
