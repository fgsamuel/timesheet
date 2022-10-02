import pytest
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.urls import reverse


@pytest.mark.django_db
class TestUsersEndpoint:
    def test_list_users_successfully(self, authenticated_client):
        endpoint = reverse("users-list")
        response = authenticated_client.get(endpoint, format="json")
        assert response.status_code == 200

    def test_get_user_successfully(self, authenticated_client):
        user = User.objects.create_user(username="teste", first_name="User")
        endpoint = reverse("users-detail", kwargs={"pk": user.id})
        response = authenticated_client.get(endpoint, format="json")
        assert response.data["name"] == user.first_name

    def test_created_user_should_be_able_to_authenticate(self, authenticated_client):
        endpoint = reverse("users-list")
        data = {"name": "User 01", "email": "user01@email.com", "login": "user01", "password": "user01"}
        authenticated_client.post(endpoint, data=data, format="json")
        user = authenticate(login=data["login"], password=data["password"])
        assert user

    def test_create_shold_not_show_password(self, authenticated_client):
        endpoint = reverse("users-list")
        data = {"name": "User 01", "email": "user01@email.com", "login": "user01", "password": "user01"}
        result = authenticated_client.post(endpoint, data=data, format="json")
        assert "password" not in result.data.keys()

    def test_update_should_return_successfully(self, authenticated_client):
        user = User.objects.create_user(username="teste", first_name="Teste")
        endpoint = reverse("users-detail", kwargs={"pk": user.id})
        data = {"name": "User 01", "email": "user01@email.com", "login": "user01"}
        result = authenticated_client.put(endpoint, data=data, format="json")
        assert result.status_code == 200
