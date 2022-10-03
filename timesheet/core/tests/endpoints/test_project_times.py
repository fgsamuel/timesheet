from datetime import timedelta

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient

from timesheet.core.models import Project
from timesheet.core.models import ProjectTime


@pytest.mark.django_db
class TestProjectTimesEndpoint:
    def test_list_times_successfully(self, authenticated_client):
        endpoint = reverse("projecttimes-list")
        response = authenticated_client.get(endpoint, format="json")
        assert response.status_code == 200

    def test_get_time_successfully(self, authenticated_client):
        user = User.objects.create_user("User")
        project = Project.objects.create(title="Project 01", description="Project 01")
        time = ProjectTime.objects.create(
            project=project, user=user, started_at="2022-10-01 20:00:00", ended_at="2022-10-01 21:00:00"
        )
        endpoint = reverse("projecttimes-detail", kwargs={"pk": time.id})
        response = authenticated_client.get(endpoint, format="json")
        assert response.data["project"] == project.id

    def test_update_should_return_successfully(self, authenticated_client):
        user = User.objects.create_user("User")
        project = Project.objects.create(title="Project 01", description="Project 01")
        data = {
            "project": project.id,
            "user": user.id,
            "started_at": "2022-10-01T20:00:00Z",
            "ended_at": "2022-10-01T22:00:00Z",
        }
        time = ProjectTime.objects.create(
            project=project, user=user, started_at="2022-10-01T20:00:00Z", ended_at="2022-10-01T21:00:00Z"
        )
        endpoint = reverse("projecttimes-detail", kwargs={"pk": time.id})
        data["ended_at"] = "2022-10-01 22:00:00"
        response = authenticated_client.put(endpoint, data=data, format="json")
        assert response.data["ended_at"] == "2022-10-01T22:00:00Z"

    def test_user_list_only_its_times(self):
        end_time = timezone.now()
        start_time = end_time - timedelta(hours=1)
        user1 = User.objects.create_user("User1")
        user2 = User.objects.create_user("User2")
        project = Project.objects.create(title="Project 01", description="Project 01")
        ProjectTime.objects.create(user=user1, project=project, started_at=start_time, ended_at=end_time)
        ProjectTime.objects.create(user=user2, project=project, started_at=start_time, ended_at=end_time)

        endpoint = reverse("projecttimes-list")
        client = APIClient()
        client.force_authenticate(user=user1)
        result = client.get(endpoint, format="json")
        assert len(result.data) == 1
        assert result.data[0]["user"] == user1.id

    def test_user_update_time_not_owned_raise_not_found(self):
        user = User.objects.create_user("User")
        user2 = User.objects.create_user("User2")
        project = Project.objects.create(title="Project 01", description="Project 01")
        data = {
            "project": project.id,
            "user": user.id,
            "started_at": "2022-10-01T20:00:00Z",
            "ended_at": "2022-10-01T22:00:00Z",
        }
        time = ProjectTime.objects.create(
            project=project, user=user, started_at="2022-10-01T20:00:00Z", ended_at="2022-10-01T21:00:00Z"
        )
        endpoint = reverse("projecttimes-detail", kwargs={"pk": time.id})
        data["ended_at"] = "2022-10-01 22:00:00"
        client = APIClient()
        client.force_authenticate(user=user2)
        response = client.put(endpoint, data=data, format="json")
        assert response.status_code == 404

    def test_user_create_time_in_project_not_owned_by_should_raise_not_found(self):
        user = User.objects.create_user("User")
        project = Project.objects.create(title="Project 01", description="Project 01")
        data = {
            "project": project.id,
            "user": user.id,
            "started_at": "2022-10-01T20:00:00Z",
            "ended_at": "2022-10-01T22:00:00Z",
        }
        endpoint = reverse("projecttimes-list")
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.post(endpoint, data=data, format="json")
        assert response.status_code == 404

    def test_user_update_time_in_project_not_owned_by_should_raise_not_found(self):
        user = User.objects.create_user("User")
        user2 = User.objects.create_user("User2")
        project = Project.objects.create(title="Project 01", description="Project 01")
        time = ProjectTime.objects.create(
            project=project, user=user2, started_at="2022-10-01 20:00:00", ended_at="2022-10-01 21:00:00"
        )
        data = {
            "project": project.id,
            "user": user.id,
            "started_at": "2022-10-01T20:00:00Z",
            "ended_at": "2022-10-01T22:00:00Z",
        }
        endpoint = reverse("projecttimes-detail", kwargs={"pk": time.id})
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.put(endpoint, data=data, format="json")
        assert response.status_code == 404

    def test_user_update_its_time_in_project_successfully(self):
        user = User.objects.create_user("User")
        project = Project.objects.create(title="Project 01", description="Project 01")
        time = ProjectTime.objects.create(
            project=project, user=user, started_at="2022-10-01 20:00:00", ended_at="2022-10-01 21:00:00"
        )
        data = {
            "project": project.id,
            "user": user.id,
            "started_at": "2022-10-01T20:00:00Z",
            "ended_at": "2022-10-01T23:00:00Z",
        }
        endpoint = reverse("projecttimes-detail", kwargs={"pk": time.id})
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.put(endpoint, data=data, format="json")
        assert response.data["ended_at"] == "2022-10-01T23:00:00Z"

    def test_admin_update_time_in_project_successfully(self, authenticated_client):
        user = User.objects.create_user("User")
        project = Project.objects.create(title="Project 01", description="Project 01")
        time = ProjectTime.objects.create(
            project=project, user=user, started_at="2022-10-01 20:00:00", ended_at="2022-10-01 21:00:00"
        )
        data = {
            "project": project.id,
            "user": user.id,
            "started_at": "2022-10-01T20:00:00Z",
            "ended_at": "2022-10-01T23:00:00Z",
        }
        endpoint = reverse("projecttimes-detail", kwargs={"pk": time.id})
        response = authenticated_client.put(endpoint, data=data, format="json")
        assert response.data["ended_at"] == "2022-10-01T23:00:00Z"

    def test_user_create_time_in_its_project_successfully(self):
        user = User.objects.create_user("User")
        project = Project.objects.create(title="Project 01", description="Project 01")
        project.users.set([user.id])
        data = {
            "project": project.id,
            "user": user.id,
            "started_at": "2022-10-01T20:00:00Z",
            "ended_at": "2022-10-01T22:00:00Z",
        }
        endpoint = reverse("projecttimes-list")
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.post(endpoint, data=data, format="json")
        assert response.status_code == 201
