from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import viewsets

from timesheet.core.api.v1.serializers import UserCreateSerializer
from timesheet.core.api.v1.serializers import UserSerializer


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
