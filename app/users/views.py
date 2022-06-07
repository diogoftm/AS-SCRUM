from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout as django_logout
from .forms import UserRegisterForm
from guardian.shortcuts import assign_perm
from scrum.models import Project, Task
from .models import UserProfile


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            UserProfile.objects.create(user= user)
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def logout(request, **kwargs):
    messages.success(request, 'Logged out.')
    django_logout(request)
    return redirect('home')


@login_required
def personal_dashboard(request):
    user_prof = UserProfile.objects.filter(user=request.user).first()
    tasks = []
    points=0
    projs = user_prof.projects.all()
    if projs.count() == 0:
        return render(request, 'users/personal_dashboard.html', {'title': f"{request.user.username}'s dashboard",
                                                             'projects': tasks, 'n_tasks': 0,
                                                                 'n_projects': 0, 'n_points': 0}) #, 'tasks': tasks

    for proj in projs :
        for task in proj.tasks.all():
            for user in task.assigned_for.all():
                if user == request.user:
                    tasks.append(task)
                    points = points + task.points

    dict={
        "Todo":0,
        "Inprogress":0,
        "Done":0
    }
    for task in tasks:
        if task.state == 1:
          dict['Todo'] += 1
        elif task.state == 2:
            dict['Inprogress'] += 1
        elif task.state == 3 or task.state == 4:
            dict['Done'] += 1
        

    return render(request, 'users/personal_dashboard.html', {'title': f"{user_prof.projects.first().title}'s dashboard",
                                                             'projects': user_prof.projects.all().values(),
                                                             'tasks': tasks, 'n_tasks': tasks.__len__(),
                                                             'n_projects': projs.count(), 'n_points': points,
                                                             'graf': dict})


