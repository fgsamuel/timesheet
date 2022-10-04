import pytest
from django.contrib.auth import authenticate
from django.forms import model_to_dict
from django.urls import reverse
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestUsersEndpoint:
    def test_list_users_successfully(self, authenticated_client):
        endpoint = reverse("users-list")
        response = authenticated_client.get(endpoint, format="json")
        assert response.status_code == 200

    def test_get_user_successfully(self, authenticated_client, user):
        endpoint = reverse("users-detail", kwargs={"pk": user.id})
        response = authenticated_client.get(endpoint, format="json")
        assert response.data["name"] == user.first_name

    def test_created_user_should_be_able_to_authenticate(self, authenticated_client, user_factory):
        endpoint = reverse("users-list")
        data = model_to_dict(user_factory.build(password="test"))
        authenticated_client.post(endpoint, data=data, format="json")
        user = authenticate(login=data["username"], password=data["password"])
        assert user

    def test_create_shold_not_show_password(self, authenticated_client, user_factory):
        endpoint = reverse("users-list")
        data = model_to_dict(user_factory.build(password="test"))
        result = authenticated_client.post(endpoint, data=data, format="json")
        assert "password" not in result.data.keys()

    def test_update_should_return_successfully(self, authenticated_client, user):
        endpoint = reverse("users-detail", kwargs={"pk": user.id})
        data = {**model_to_dict(user), "password": "test"}
        result = authenticated_client.put(endpoint, data=data, format="json")
        assert result.status_code == 200

    def test_admin_list_all_users(self, authenticated_client, user_factory):
        user_factory.create_batch(2)
        endpoint = reverse("users-list")
        result = authenticated_client.get(endpoint, format="json")
        assert len(result.data) == 3

    def test_user_can_list_only_itself(self, user_factory):
        users = user_factory.create_batch(2)
        endpoint = reverse("users-list")
        client = APIClient()
        client.force_authenticate(user=users[0])
        result = client.get(endpoint, format="json")
        assert len(result.data) == 1
        assert result.data[0]["name"] == users[0].first_name

    def test_user_cant_create_user(self, user):
        endpoint = reverse("users-list")
        client = APIClient()
        client.force_authenticate(user=user)
        data = {"name": "User 01", "email": "user01@email.com", "login": "user01", "password": "user01"}
        result = client.post(endpoint, data=data, format="json")
        assert result.status_code == 403
