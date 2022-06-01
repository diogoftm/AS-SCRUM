from django.contrib.auth.models import User
from django.db import models
from scrum.models import Project


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    projects = models.ManyToManyField(Project)

