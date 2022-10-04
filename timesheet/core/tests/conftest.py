from pytest_factoryboy import register

from timesheet.core.factories import ProjectFactory
from timesheet.core.factories import ProjectTimeFactory
from timesheet.core.factories import UserFactory

register(UserFactory)
register(ProjectFactory)
register(ProjectTimeFactory)
