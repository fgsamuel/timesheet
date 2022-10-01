import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestAuthenticateEndpoint:
    endpoint = reverse("token_obtain_pair")

    def get_response(self, data):
        client = APIClient()
        response = client.post(self.endpoint, data, format="json")
        return response

    def test_success_authenticate_should_have_token_and_user(self):
        admin = User.objects.create_superuser(username="admin")
        admin.set_password("admin")
        admin.save()

        response = self.get_response({"login": "admin", "password": "admin"})

        assert {"user", "token"} == set(response.data.keys())

    def test_invalid_login_should_rais_401(self):
        response = self.get_response({"login": "admin", "password": "admin"})
        assert response.status_code == 401
