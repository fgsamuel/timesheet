import pytest
from django.forms import model_to_dict
from django.urls import reverse
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestProjectTimesEndpoint:
    def test_list_times_successfully(self, authenticated_client):
        endpoint = reverse("projecttimes-list")
        response = authenticated_client.get(endpoint, format="json")
        assert response.status_code == 200

    def test_get_time_successfully(self, authenticated_client, project_time):
        endpoint = reverse("projecttimes-detail", kwargs={"pk": project_time.id})
        response = authenticated_client.get(endpoint, format="json")
        assert response.data["project"] == project_time.id

    def test_update_should_return_successfully(self, authenticated_client, project_time):
        endpoint = reverse("projecttimes-detail", kwargs={"pk": project_time.id})
        data = {**model_to_dict(project_time), "ended_at": "2022-10-01T22:00:00Z"}
        response = authenticated_client.put(endpoint, data=data, format="json")
        assert response.data["ended_at"] == "2022-10-01T22:00:00Z"

    def test_user_list_only_its_times(self, user, project_time_factory):
        project_time_factory()
        project_time_factory(user=user)

        endpoint = reverse("projecttimes-list")
        client = APIClient()
        client.force_authenticate(user=user)
        result = client.get(endpoint, format="json")
        assert len(result.data) == 1
        assert result.data[0]["user"] == user.id

    def test_user_update_time_not_owned_raise_not_found(self, user, project_time_factory):
        project_time = project_time_factory()
        data = model_to_dict(project_time)
        endpoint = reverse("projecttimes-detail", kwargs={"pk": project_time.id})
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.put(endpoint, data=data, format="json")
        assert response.status_code == 404

    def test_user_create_time_in_project_not_owned_by_should_raise_not_found(self, user, project_time):
        data = model_to_dict(project_time)
        endpoint = reverse("projecttimes-list")
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.post(endpoint, data=data, format="json")
        assert response.status_code == 404

    def test_user_update_its_time_in_project_successfully(self, project_time):
        data = model_to_dict(project_time)
        endpoint = reverse("projecttimes-detail", kwargs={"pk": project_time.id})
        client = APIClient()
        client.force_authenticate(user=project_time.user)
        response = client.put(endpoint, data=data, format="json")
        assert response.status_code == 200

    def test_admin_update_time_in_project_successfully(self, authenticated_client, project_time):
        data = model_to_dict(project_time)
        endpoint = reverse("projecttimes-detail", kwargs={"pk": project_time.id})
        response = authenticated_client.put(endpoint, data=data, format="json")
        assert response.status_code == 200

    def test_user_create_time_in_its_project_successfully(self, user, project, project_time_factory):
        project.users.set([user.id])
        data = model_to_dict(project_time_factory.build(user=user, project=project))
        endpoint = reverse("projecttimes-list")
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.post(endpoint, data=data, format="json")
        assert response.status_code == 201
