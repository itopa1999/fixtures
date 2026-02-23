"""
Admin View Serializers
"""

from rest_framework import serializers
from django.contrib.auth.models import User


class AdminLoginSerializer(serializers.Serializer):
    """
    Serializer for admin login
    """
    username = serializers.CharField(
        required=True,
        allow_blank=False,
        trim_whitespace=True,
        help_text='Admin username'
    )
    password = serializers.CharField(
        required=True,
        allow_blank=False,
        write_only=True,
        help_text='Admin password'
    )

    def validate_username(self, value):
        """Validate username exists"""
        if not value:
            raise serializers.ValidationError('Username cannot be empty')
        return value

    def validate_password(self, value):
        """Validate password"""
        if not value:
            raise serializers.ValidationError('Password cannot be empty')
        return value


class AdminUserSerializer(serializers.ModelSerializer):
    """
    Serializer for admin user details
    """
    groups = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name', 'groups'
        )
        read_only_fields = fields

    def get_groups(self, obj):
        """Get user groups"""
        return [group.name for group in obj.groups.all()]
