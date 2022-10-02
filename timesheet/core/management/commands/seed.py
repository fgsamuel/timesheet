from datetime import timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from timesheet.core.models import Project
from timesheet.core.models import ProjectTime


class Command(BaseCommand):
    help = "Create fake data for testing purposes"

    def handle(self, *args, **options):
        admin, _ = User.objects.update_or_create(username="admin", defaults={"first_name": "Admin"})
        admin.is_staff = True
        admin.is_superuser = True
        admin.set_password("admin")
        admin.save()

        users_ids = []

        for i in range(1, 11):
            name = f"User {str(i).zfill(2)}"
            username = f"user{str(i).zfill(2)}"
            user, _ = User.objects.update_or_create(username=username, defaults={"first_name": name})
            user.set_password(username)
            user.save()
            users_ids.append(user.id)

        for i in range(1, 11):
            name = f"Project {str(i).zfill(2)}"
            project, _ = Project.objects.update_or_create(title=name, defaults={"description": name})
            project.users.set(users_ids)
            project.save()

        user = User.objects.first()
        project = Project.objects.first()
        start_time = timezone.now()
        end_time = start_time - timedelta(days=1)
        for i in range(1, 11):
            start_time -= timedelta(days=1)
            end_time -= timedelta(days=1)
            ProjectTime.objects.update_or_create(
                user=user,
                project=project,
                started_at__date=start_time.date(),
                defaults={"started_at": start_time, "ended_at": end_time},
            )

        self.stdout.write(self.style.SUCCESS("Successfully seed"))
