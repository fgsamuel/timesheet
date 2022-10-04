import random
from datetime import timedelta

import factory
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.utils import timezone
from factory.django import DjangoModelFactory

from timesheet.core.models import Project
from timesheet.core.models import ProjectTime


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.Faker("user_name")
    email = factory.LazyAttribute(lambda o: f"{o.username}@email.com")
    password = factory.LazyAttribute(lambda o: make_password(o.username))


class ProjectFactory(DjangoModelFactory):
    class Meta:
        model = Project

    title = factory.Faker("color_name")
    description = factory.Faker("color_name")


class ProjectTimeFactory(DjangoModelFactory):
    class Meta:
        model = ProjectTime

    project = factory.SubFactory(ProjectFactory)
    user = factory.SubFactory(UserFactory)
    started_at = factory.LazyAttribute(lambda o: timezone.now() - timedelta(minutes=random.randint(120, 180)))
    ended_at = factory.LazyAttribute(lambda o: timezone.now() - timedelta(minutes=random.randint(0, 60)))
