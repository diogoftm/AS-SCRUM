from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages
from django.shortcuts import render
from users.models import UserProfile
from users import views as user_views
from django.contrib.auth.models import User
from .models import Task,Project,Sprint
from .forms import *
from django.http import HttpResponseRedirect


def home(request):
    if request.user.is_authenticated:
        return user_views.personal_dashboard(request)

    return render(request,'scrum/index.html', {'title': 'Home'})


def project(request, project_id=None):
    user_prof = UserProfile.objects.filter(user=request.user).first()
    proj = Project.objects.filter(id=project_id)
    return render(request, 'scrum/project_overview.html', {'title': f"{proj.first().title} dashboard",
                                                             'permission': request.user.has_perm('master',
                                                                                                 user_prof.projects.first()),
                                                             'projects': user_prof.projects.all().values(),
                                                             'project': proj.values()[0],
                                                             'sprints': proj.first().sprints.values(),
                                                             'team': User.objects.filter(groups__id=proj.first().group.id).values()})

@login_required
def new_task(request, project_id=None):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            task = Task.objects.create(title=data.get('title'), annotations=data.get('annotations'),
                                       as_a=data.get('as_a'), i_want=data.get('i_want'),
                                       so_that=data.get('so_that'), points=data.get('points'),
                                       priority=data.get('priority'), created_by=request.user, state=1)
            for user in data.get('assign_for'):
                task.assigned_for.add(user)
            task.save()
            Project.objects.filter(id=project_id).first().tasks.add(task)
            return HttpResponseRedirect(f'/projects/{project_id}')

    else:
        user_prof = UserProfile.objects.filter(user=request.user).first()
        form = TaskForm(**{'project': project_id})
    return render(request, 'scrum/creation_form.html', {'title': f"new task", 'form': form, 'projects': user_prof.projects.all().values(), })


@login_required
def new_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            proj = Project.objects.create(title=data.get('title'), description=data.get('description'),
                                       created_by=request.user, sprint_duration=data.get('sprint_duration'), state=1,
                                       password=data.get('password'), group_id=1)
            group = Group.objects.get_or_create(name=f'Project {proj.id}')
            group[0].user_set.add(request.user)
            proj.group_id = group[0].id
            proj.save()
            UserProfile.objects.filter(user=request.user).first().projects.add(proj)
            messages.success(request, f'Project with id= {proj.id} was created!')
            return HttpResponseRedirect(f'/projects/{proj.id}')
    else:
        user_prof = UserProfile.objects.filter(user=request.user).first()
        form = ProjectForm()
        return render(request, 'scrum/creation_form.html', {'title': f"new project", 'form': form, 'projects': user_prof.projects.all().values()})


@login_required
def product_backlog(request, project_id=None):
    proj = Project.objects.filter(id=project_id).first()
    user_prof = UserProfile.objects.filter(user=request.user).first()
    return render(request, 'scrum/product_backlog.html', {'title': f"Product Backlog", 'projects': user_prof.projects.all().values(), 'tasks': proj.tasks.values(),
                                                          'sprints': proj.sprints.values(),'project': proj})


@login_required
def add_task_sprint(request, project_id=None):
    proj = Project.objects.filter(id=project_id).first()
    task = proj.tasks.filter(id=request.POST.get("task_id")).first()
    sprint = proj.sprints.filter(number=request.POST.get("sprint_number")).first()
    sprint.tasks.add(task)
    messages.success(request, f'tarefa adicionada ao sprint {request.POST.get("sprint_number")}!')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def create_sprint(request, project_id=None):
    proj = Project.objects.filter(id=project_id).first()
    n = proj.sprints.count() + 1
    sprint = Sprint.objects.create(number=n, state=1)
    sprint.save()
    proj.sprints.add(sprint)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def sprint(request, project_id=None, sprint_number=None):
    tasks = Project.objects.filter(id=project_id).first().sprints.filter(number=sprint_number).first().tasks.values()
    user_prof = UserProfile.objects.filter(user=request.user).first()
    return render(request, 'scrum/sprint.html', {'title': f"Product Backlog", 'tasks': tasks, 'projects': user_prof.projects.all().values(), 'n': sprint_number})


@login_required
def join_project(request):
    if request.method == 'POST':
        form = JoinProjectForm(request.POST)
        if form.is_valid():
            print("AQUI")
            data = form.cleaned_data
            proj = Project.objects.filter(id=data.get("id")).first()
            if data.get("password") == proj.password:
                print("password correta")
                user_prof = UserProfile.objects.filter(user=request.user).first()
                user_prof.projects.add(proj)
                group = Group.objects.get(name=f'Project {data.get("id")}')
                group.user_set.add(request.user)
                messages.success(request, f'Success!')
                return project(request, data.get("id"))
            else:
                messages.success(request, f'Incorrect password or wrong project id!')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            user_prof = UserProfile.objects.filter(user=request.user).first()
            form = JoinProjectForm()
            return render(request, 'scrum/creation_form.html',
                          {'title': f"join a project", 'form': form, 'projects': user_prof.projects.all().values()})
    else:
        user_prof = UserProfile.objects.filter(user=request.user).first()
        form = JoinProjectForm()
        return render(request, 'scrum/creation_form.html',
                      {'title': f"join a project", 'form': form, 'projects': user_prof.projects.all().values()})


@login_required
def change_task_state(request):
    task = Task.objects.filter(id=request.POST.get("task_id")).first()
    task.state = request.POST.get("state")
    task.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
