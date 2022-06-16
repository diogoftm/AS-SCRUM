from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render
from users.models import UserProfile
from .models import Project
from django.contrib.auth.models import User
from .models import Task
from .forms import TaskForm, ProjectForm
from django.http import HttpResponseRedirect

