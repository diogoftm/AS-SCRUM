from django.db import models
from django.contrib.auth.models import User, Group


class Task(models.Model):
    title = models.TextField()
    as_a = models.TextField()
    i_want = models.TextField()
    so_that = models.TextField()
    annotations = models.TextField()
    points = models.IntegerField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by+')
    created_at = models.DateTimeField(auto_now_add=True)
    assigned_for = models.ManyToManyField(User)
    priority = models.IntegerField()

    TODO = 1
    IN_PROGRESS = 2
    FINISHED = 3

    STATE_CHOICES = (
        (TODO, 'To Do'),
        (IN_PROGRESS, 'In Progress'),
        (FINISHED, 'Finished'),
    )
    state = models.PositiveSmallIntegerField(choices=STATE_CHOICES, blank=True, null=True)


class Sprint(models.Model):
    number = models.IntegerField()
    tasks = models.ManyToManyField(Task)
    created_at = models.DateTimeField(auto_now_add=True)

    TO_START = 1
    IN_PROGRESS = 2
    FINISHED = 3

    STATE_CHOICES = (
        (TO_START, "To Start"),
        (IN_PROGRESS, 'In Progress'),
        (FINISHED, 'Finished'),
    )
    state = models.PositiveSmallIntegerField(choices=STATE_CHOICES, blank=True, null=True)


class Project(models.Model):
    title = models.TextField()
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from+')
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    tasks = models.ManyToManyField(Task)
    sprints = models.ManyToManyField(Sprint)
    sprint_duration = models.IntegerField()
    password = models.TextField()

    IN_PROGRESS = 1
    FINISHED = 2

    STATE_CHOICES = (
        (IN_PROGRESS, 'In Progress'),
        (FINISHED, 'Finished'),
    )
    state = models.PositiveSmallIntegerField(choices=STATE_CHOICES, blank=True, null=True)

    class Meta:
        permissions = (
            ('master', 'Master Permissions'),
            ('developer', 'Developer Permissions'),
            ('boss', 'Boss Permissions'),
        )

