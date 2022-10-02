from django.contrib import admin

from timesheet.core.models import Project, ProjectTime

admin.site.register(Project)
admin.site.register(ProjectTime)
