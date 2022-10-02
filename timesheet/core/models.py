from django.db import models


class Project(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255)
    users = models.ManyToManyField("auth.User", related_name="projects", blank=True)

    def __str__(self):
        return self.title


class ProjectTime(models.Model):
    project = models.ForeignKey("Project", on_delete=models.CASCADE, related_name="times")
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="times")
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField()

    def __str__(self):
        return f"{self.project} - {self.user} - {self.started_at.date()}"
