import pytest
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestUsersEndpoint:
    def test_list_users_successfully(self):
        admin = User.objects.create_superuser(username="admin")
        endpoint = reverse("users-list")
        client = APIClient()
        client.force_authenticate(user=admin)
        response = client.get(endpoint, format="json")
        assert response.status_code == 200

    def test_get_user_successfully(self):
        admin = User.objects.create_superuser(username="admin")
        endpoint = reverse("users-detail", kwargs={"pk": admin.id})
        client = APIClient()
        client.force_authenticate(user=admin)
        response = client.get(endpoint, format="json")
        assert response.data["name"] == admin.first_name

    def test_created_user_should_be_able_to_authenticate(self):
        admin = User.objects.create_superuser(username="admin")
        endpoint = reverse("users-list")
        client = APIClient()
        client.force_authenticate(user=admin)
        data = {"name": "User 01", "email": "user01@email.com", "login": "user01", "password": "user01"}
        client.post(endpoint, data=data, format="json")
        user = authenticate(login=data["login"], password=data["password"])
        assert user

    def test_create_shold_not_show_password(self):
        admin = User.objects.create_superuser(username="admin")
        endpoint = reverse("users-list")
        client = APIClient()
        client.force_authenticate(user=admin)
        data = {"name": "User 01", "email": "user01@email.com", "login": "user01", "password": "user01"}
        result = client.post(endpoint, data=data, format="json")
        assert "password" not in result.data.keys()

    def test_update_should_return_successfully(self):
        admin = User.objects.create_superuser(username="admin")
        endpoint = reverse("users-detail", kwargs={"pk": admin.id})
        client = APIClient()
        client.force_authenticate(user=admin)
        data = {"name": "User 01", "email": "user01@email.com", "login": "user01"}
        result = client.put(endpoint, data=data, format="json")
        assert result.status_code == 200
