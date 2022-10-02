from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import viewsets

from timesheet.core.api.v1.serializers import ProjectDetailSerializer
from timesheet.core.api.v1.serializers import ProjectSerializer
from timesheet.core.api.v1.serializers import UserCreateSerializer
from timesheet.core.api.v1.serializers import UserSerializer
from timesheet.core.models import Project


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        return UserSerializer

    def perform_create(self, serializer):
        with transaction.atomic():
            obj = serializer.save()
            obj.set_password(serializer.initial_data["password"])
            obj.save()


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return ProjectSerializer
        return ProjectDetailSerializer
