"""
Serializers for the user API view
"""

from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext as _

from rest_framework import serializers


class UserSerializer(
    serializers.ModelSerializer
):  # ModelSerializer is used for creating and validating for a Django database model
    """Serializer for the user object."""

    class Meta:  # Defines the model and fields for the serisalizer
        model = get_user_model()

        # Fields provided in the request
        fields = ["email", "password", "name"]

        # Extra settings for the fields
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        """Create and return a user with encrypted password"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update and return user."""
        password = validated_data.pop(
            "password", None
        )  # if password is not given, give None

        # The instance is the object to be updated (In this case model object)
        user = super().update(
            instance, validated_data
        )  # use the base class's update method

        if password:
            user.set_password(password)
            user.save()
        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token."""

    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user."""
        email = attrs.get("email")
        password = attrs.get("password")
        user = authenticate(
            request=self.context.get("request"), username=email, password=password
        )  # if the credentials are valid, returns the user object, otherwise None
        if not user:
            msg = _("Unable to authenticate with provided credentials.")
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs
