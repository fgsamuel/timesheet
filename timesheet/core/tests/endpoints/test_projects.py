import pytest
from django.forms.models import model_to_dict
from django.urls import reverse
from rest_framework.test import APIClient

from timesheet.core.models import Project


@pytest.mark.django_db
class TestProjectsEndpoint:
    def test_list_projects_successfully(self, authenticated_client):
        endpoint = reverse("projects-list")
        response = authenticated_client.get(endpoint, format="json")
        assert response.status_code == 200

    def test_get_project_successfully(self, authenticated_client, project_factory):
        project = project_factory()
        endpoint = reverse("projects-detail", kwargs={"pk": project.id})
        response = authenticated_client.get(endpoint, format="json")
        assert response.data["title"] == project.title

    def test_created_project_with_users_successfully(self, authenticated_client, user_factory, project_factory):
        users = [user.id for user in user_factory.create_batch(3)]
        endpoint = reverse("projects-list")
        data = {**model_to_dict(project_factory.build()), "users": users}
        authenticated_client.post(endpoint, data=data, format="json")
        project = Project.objects.get(title=data["title"])
        assert project.users.all().count() == 3

    def test_update_should_return_successfully(self, authenticated_client, project):
        endpoint = reverse("projects-detail", kwargs={"pk": project.id})
        data = {**model_to_dict(project), "title": "new title"}
        result = authenticated_client.put(endpoint, data=data, format="json")
        assert result.status_code == 200

    def test_user_list_only_its_projects(self, user_factory, project_factory):
        users = [user for user in user_factory.create_batch(2)]
        projects = [project for project in project_factory.create_batch(2)]
        projects[0].users.set([users[0].id, users[1].id])
        projects[1].users.set([users[1].id])

        endpoint = reverse("projects-list")
        client = APIClient()
        client.force_authenticate(user=users[0])
        result = client.get(endpoint, format="json")

        assert len(result.data) == 1
        assert result.data[0]["title"] == projects[0].title

    def test_admin_list_all_projects(self, authenticated_client, project_factory):
        project_factory.create_batch(2)

        endpoint = reverse("projects-list")
        result = authenticated_client.get(endpoint, format="json")

        assert len(result.data) == 2

    def test_user_cant_create_project(self, user, project_factory):
        endpoint = reverse("projects-list")
        data = model_to_dict(project_factory.build())
        client = APIClient()
        client.force_authenticate(user=user)
        result = client.post(endpoint, data=data, format="json")
        assert result.status_code == 403

    def test_user_cant_update_project(self, user, project):
        project.users.set([user.id])
        endpoint = reverse("projects-detail", kwargs={"pk": project.id})
        data = {"title": "Project 01", "description": "Project 01", "users": []}
        client = APIClient()
        client.force_authenticate(user=user)
        result = client.put(endpoint, data=data, format="json")
        assert result.status_code == 403

    def test_user_cant_delete_project(self, user, project):
        project.users.set([user.id])
        endpoint = reverse("projects-detail", kwargs={"pk": project.id})
        client = APIClient()
        client.force_authenticate(user=user)
        result = client.delete(endpoint, format="json")
        assert result.status_code == 403

    def test_admin_can_delete_project(self, authenticated_client, project):
        endpoint = reverse("projects-detail", kwargs={"pk": project.id})
        result = authenticated_client.delete(endpoint, format="json")
        assert result.status_code == 204
