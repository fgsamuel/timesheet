from django.contrib.auth.models import User
from django.db import transaction
from django.http import Http404
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied

from timesheet.core.api.v1.serializers import ProjectDetailSerializer
from timesheet.core.api.v1.serializers import ProjectSerializer
from timesheet.core.api.v1.serializers import ProjectTimeSerializer
from timesheet.core.api.v1.serializers import UserCreateSerializer
from timesheet.core.api.v1.serializers import UserSerializer
from timesheet.core.models import Project
from timesheet.core.models import ProjectTime


class UserViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        return UserSerializer

    def perform_create(self, serializer):
        with transaction.atomic():
            obj = serializer.save()
            obj.set_password(serializer.initial_data["password"])
            obj.save()

    def create(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied("Only admin can create user")
        return super().create(request, *args, **kwargs)


class ProjectViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Project.objects.all()
        return Project.objects.filter(users=self.request.user.id)

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return ProjectSerializer
        return ProjectDetailSerializer

    def create(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied("Only admin can create project")
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied("Only admin can update project")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied("Only admin can delete project")
        return super().destroy(request, *args, **kwargs)


class ProjectTimeViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectTimeSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return ProjectTime.objects.all()
        return ProjectTime.objects.filter(user_id=self.request.user.id)

    def create(self, request, *args, **kwargs):
        user = request.user
        project = request.data.get("project")
        if project and (user.is_superuser or not user.projects.filter(id=project).first()):
            raise Http404("Project not found")
        return super().create(request, *args, **kwargs)
