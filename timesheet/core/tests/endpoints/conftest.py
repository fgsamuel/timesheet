import pytest
from rest_framework.test import APIClient


@pytest.fixture
def authenticated_client(user_factory):
    admin = user_factory(is_superuser=True)
    client = APIClient()
    client.force_authenticate(user=admin)
    return client
