from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    name = serializers.CharField(required=True, source="first_name")

    class Meta:
        model = User
        fields = ("id", "name", "username", "email")
