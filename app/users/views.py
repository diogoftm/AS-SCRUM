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
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('home')
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
    for proj in user_prof.projects.all():
        for task in proj.tasks.all():
            for user in task.assigned_for.all():
                if user == request.user:
                    tasks.append(task)

    return render(request, 'users/personal_dashboard.html', {'title': f"{user_prof.projects.first().title}'s dashboard",
                                                             'projects': user_prof.projects.all().values()}) #, 'tasks': tasks


