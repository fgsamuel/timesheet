from django.urls import include
from django.urls import path
from rest_framework import routers

from timesheet.core.api.v1.views import UserViewSet

router = routers.DefaultRouter()
router.register(r"users", UserViewSet, basename="users")

urlpatterns = [
    path("", include(router.urls)),
]
