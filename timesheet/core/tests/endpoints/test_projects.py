import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from timesheet.core.models import Project


@pytest.mark.django_db
class TestProjectsEndpoint:
    def test_list_projects_successfully(self, authenticated_client):
        endpoint = reverse("projects-list")
        response = authenticated_client.get(endpoint, format="json")
        assert response.status_code == 200

    def test_get_project_successfully(self, authenticated_client):
        project = Project.objects.create(title="Project 01", description="Project 01")
        endpoint = reverse("projects-detail", kwargs={"pk": project.id})
        response = authenticated_client.get(endpoint, format="json")
        assert response.data["title"] == project.title

    def test_created_project_with_users_successfully(self, authenticated_client):
        user1 = User.objects.create_user(username="user1", password="user1", email="user1@email.com")
        user2 = User.objects.create_user(username="user2", password="user2", email="user2@email.com")
        user3 = User.objects.create_user(username="user3", password="user3", email="user3@email.com")
        endpoint = reverse("projects-list")
        data = {"title": "Project 01", "description": "Project 01", "users": [user1.id, user2.id, user3.id]}
        authenticated_client.post(endpoint, data=data, format="json")
        project = Project.objects.get(title=data["title"])
        assert project.users.all().count() == 3

    def test_update_should_return_successfully(self, authenticated_client):
        project = Project.objects.create(title="Project 01", description="Project 01")
        endpoint = reverse("projects-detail", kwargs={"pk": project.id})
        data = {"title": "Project 01", "description": "Project 01", "users": []}
        result = authenticated_client.put(endpoint, data=data, format="json")
        assert result.status_code == 200
