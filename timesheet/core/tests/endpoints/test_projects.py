import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient

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

    def test_user_list_only_its_projects(self):
        user1 = User.objects.create_user(username="user1", password="user1", email="user1@email.com")
        user2 = User.objects.create_user(username="user2", password="user2", email="user2@email.com")
        project1 = Project.objects.create(title="Project01", description="Project01")
        project1.users.set([user1.id, user2.id])
        project2 = Project.objects.create(title="Project02", description="Project02")
        project2.users.set([user2.id])

        endpoint = reverse("projects-list")
        client = APIClient()
        client.force_authenticate(user=user1)
        result = client.get(endpoint, format="json")

        assert len(result.data) == 1
        assert result.data[0]["title"] == "Project01"

    def test_admin_list_all_projects(self, authenticated_client):
        user1 = User.objects.create_user(username="user1", password="user1", email="user1@email.com")
        user2 = User.objects.create_user(username="user2", password="user2", email="user2@email.com")
        project1 = Project.objects.create(title="Project01", description="Project01")
        project1.users.set([user1.id, user2.id])
        project2 = Project.objects.create(title="Project02", description="Project02")
        project2.users.set([user2.id])

        endpoint = reverse("projects-list")
        result = authenticated_client.get(endpoint, format="json")

        assert len(result.data) == 2

    def test_user_cant_create_project(self):
        user = User.objects.create_user(username="user1", password="user1", email="user1@email.com")
        endpoint = reverse("projects-list")
        data = {"title": "Project 01", "description": "Project 01", "users": []}
        client = APIClient()
        client.force_authenticate(user=user)
        result = client.post(endpoint, data=data, format="json")
        assert result.status_code == 403

    def test_user_cant_update_project(self):
        user = User.objects.create_user(username="user1", password="user1", email="user1@email.com")
        project = Project.objects.create(title="Project", description="Project")
        project.users.set([user.id])
        endpoint = reverse("projects-detail", kwargs={"pk": project.id})
        data = {"title": "Project 01", "description": "Project 01", "users": []}
        client = APIClient()
        client.force_authenticate(user=user)
        result = client.put(endpoint, data=data, format="json")
        assert result.status_code == 403

    def test_user_cant_delete_project(self):
        user = User.objects.create_user(username="user1", password="user1", email="user1@email.com")
        project = Project.objects.create(title="Project", description="Project")
        project.users.set([user.id])
        endpoint = reverse("projects-detail", kwargs={"pk": project.id})
        client = APIClient()
        client.force_authenticate(user=user)
        result = client.delete(endpoint, format="json")
        assert result.status_code == 403

    def test_admin_can_delete_project(self, authenticated_client):
        project = Project.objects.create(title="Project", description="Project")
        endpoint = reverse("projects-detail", kwargs={"pk": project.id})
        result = authenticated_client.delete(endpoint, format="json")
        assert result.status_code == 204
