import re

from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        """
        Validates the email address.

        Ensures that the email address ends with '.co.tz' or '.go.tz'.

        :param value: The email address to validate.
        :return: The validated email address.
        :raises serializers.ValidationError: If the email address does not end with '.co.tz' or '.go.tz'.
        """
        # Check if the email ends with '.co.tz' or '.go.tz'
        if not re.search(r'\.(co|go)\.tz$', value):
            raise serializers.ValidationError("Email must end with '.co.tz' or '.go.tz'")
        # Return the validated email
        return value

    def validate_phone(self, value):
        """
        Validates a phone number.

        :param value: The phone number to validate.
        :return: The validated phone number.
        :raises serializers.ValidationError: If the phone number is invalid.
        """
        # Check if the phone number starts with a + and includes digits
        country_code_pattern = r'^\+[1-9]\d{0,3}'
        country_code_match = re.match(country_code_pattern, value)

        if not country_code_match:
            raise serializers.ValidationError(
                "Invalid country code format. It should start with a + and include digits."
            )

        # Check if the phone number is in the correct format
        full_number_pattern = r'^\+255[0-9]{9}$'
        if not re.match(full_number_pattern, value):
            raise serializers.ValidationError(
                "Invalid phone number format. It should be in the format: +255XXXXXXXXX"
            )

        return value


    def create(self, validated_data):
        """
        Creates a new User instance.

        :param validated_data: The validated data from the request body.
        :return: The newly created User instance.
        """
        # Create a new User instance with the validated data
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        """
        Updates an existing User instance.

        :param instance: The existing User instance to update.
        :param validated_data: The validated data from the request body.
        :return: The updated User instance.
        """
        # Update the existing User instance with the validated data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance