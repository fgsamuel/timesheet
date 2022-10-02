from django.contrib.auth.models import User
from rest_framework import serializers

from timesheet.core.models import Project
from timesheet.core.models import ProjectTime


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    name = serializers.CharField(required=True, source="first_name")
    login = serializers.CharField(required=True, source="username")

    class Meta:
        model = User
        fields = ("id", "name", "login", "email")


class UserCreateSerializer(UserSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta(UserSerializer.Meta):
        fields = ("id", "name", "login", "email", "password")  # type: ignore


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ("id", "title", "description", "users")


class ProjectDetailSerializer(ProjectSerializer):
    users = UserSerializer(many=True)


class ProjectTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectTime
        fields = ("id", "user", "project", "started_at", "ended_at")
