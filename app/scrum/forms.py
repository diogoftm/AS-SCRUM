from django import forms
from django.contrib.auth.models import User
from .models import Project, Task


class TaskForm(forms.Form):
    title = forms.CharField(label='Title', max_length=20)
    as_a = forms.CharField(widget=forms.Textarea(attrs={'name':'as_a', 'rows':'3', 'cols':'10'}))
    i_want = forms.CharField(widget=forms.Textarea(attrs={'name':'i_want', 'rows':'3', 'cols':'10'}))
    so_that = forms.CharField(widget=forms.Textarea(attrs={'name':'so_that', 'rows':'3', 'cols':'10'}))
    CHOICES = (('1', '1'), ('2', '2'), ('4', '4'), ('8', '8'),)
    points = forms.ChoiceField(choices=CHOICES)
    CHOICES_P = (('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),)
    priority = forms.ChoiceField(choices=CHOICES_P)
    annotations = forms.CharField(widget=forms.Textarea(attrs={'name':'annotations', 'rows':'3', 'cols':'5'}))
    assign_for = forms.ModelMultipleChoiceField(queryset=User.objects.all(), widget=forms.CheckboxSelectMultiple)

    def __init__(self, *args, **kwargs):
        project_id = kwargs.pop('project', None)
        super(TaskForm, self).__init__(*args, **kwargs)
        if project_id is not None:
            self.fields['assign_for'].queryset = User.objects.filter(groups__name=Project.objects.filter(id=project_id).first().group.name)

    class Meta:
        model = Task
        fields = ('title', 'as_a', 'i_want', 'so_that', 'points', 'priority', 'assign_for', 'annotations')


class ProjectForm(forms.Form):
    title = forms.CharField(label='Title', max_length=20)
    sprint_duration = forms.IntegerField(min_value=1, max_value=10)
    description = forms.CharField(widget=forms.Textarea(attrs={'name': 'description', 'rows': '3', 'cols': '5'}))
    password = forms.CharField(label='Password', max_length=15)

    class Meta:
        model = Task
        fields = ('title', 'description', 'sprint_duration', 'password')

