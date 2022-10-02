from django.urls import include
from django.urls import path
from rest_framework import routers

from timesheet.core.api.v1.views import ProjectTimeViewSet
from timesheet.core.api.v1.views import ProjectViewSet
from timesheet.core.api.v1.views import UserViewSet

router = routers.DefaultRouter()
router.register(r"users", UserViewSet, basename="users")
router.register(r"projects", ProjectViewSet, basename="projects")
router.register(r"times", ProjectTimeViewSet, basename="projecttimes")

urlpatterns = [
    path("", include(router.urls)),
]
