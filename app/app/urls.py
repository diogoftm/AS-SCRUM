"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users import views as user_views
from scrum import views as scrum_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name="users/login.html"), name="login"),
    path('logout', user_views.logout, name="logout"),
    path('', scrum_views.home, name='home'),
    path('personal_dashboard', user_views.personal_dashboard, name='personal-dashboard'),
    path('projects/<int:project_id>', scrum_views.project, name='project-overview'),
    path('projects/<int:project_id>/add_task', scrum_views.new_task, name='new-task'),
    path('new_project', scrum_views.new_project, name='new-project'),
    path('projects/<int:project_id>/product_backlog', scrum_views.product_backlog, name='product-backlog'),
    path('projects/<int:project_id>/add_task_sprint', scrum_views.add_task_sprint, name='add-task-sprint'),
    path('projects/<int:project_id>/create_sprint', scrum_views.create_sprint, name='create-sprint'),
    path('projects/<int:project_id>/sprint<int:sprint_number>', scrum_views.sprint, name='sprint'),
    path('join_project/', scrum_views.join_project, name='join-project'),
]
