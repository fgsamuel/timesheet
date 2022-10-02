import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient


@pytest.fixture
def authenticated_client():
    admin = User.objects.create_superuser(username="admin")
    client = APIClient()
    client.force_authenticate(user=admin)
    return client
