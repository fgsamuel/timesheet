from django.contrib import admin

from timesheet.core.models import Project
from timesheet.core.models import ProjectTime

admin.site.register(Project)
admin.site.register(ProjectTime)
