import pytest
from django.contrib.auth.models import User
from django.urls import reverse

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
