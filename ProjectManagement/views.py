from django.views.generic import TemplateView, ListView
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from bootstrap_datepicker_plus.widgets import DatePickerInput
from django.urls import reverse
from django.utils.encoding import force_str
import operator
from django import forms
from django.shortcuts import redirect
from reports.models import Report
from team.models import Task, Worktime
from subcontractors.models import Subcontractor
from projects.models import Project, ProjectCategory
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.db.models import Count, Sum
from ProjectManagement.forms import AddTaskForm
from itertools import chain
import json
import datetime

User = get_user_model()

class index(LoginRequiredMixin,TemplateView):
    model = User
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_tasks = Task.objects.all()
        user_tasks = Task.objects.filter(task_asignee__username=self.request.user)
        projects_user = Project.objects.filter(project_members=self.request.user.id)
        approaching_projects = projects_user.order_by('project_delivery_date')
        pending_tasks = False
        for project in approaching_projects:
            if project.project_delivery_date < datetime.date.today():
                project.project_status = 'Delayed'
                pending_tasks = False
        try:
            for task in user_tasks:
                if task.task_status == 'Pending':
                    pending_tasks = True
        except:
            pending_tasks = False
        totalworktime = Worktime.objects.all()
        context['total_worktime'] = totalworktime
        context['daily_worktime'] = Worktime.objects.filter(worktime_user=self.request.user).filter(worktime_date=datetime.datetime.now())
        context['total_daily_worktime'] = Worktime.objects.filter(worktime_user=self.request.user).filter(worktime_date=datetime.datetime.now()).aggregate(Sum('worktime_hour'))
        context['user_tasks'] = user_tasks
        context['projects_user'] = projects_user
        context['approaching_projects'] = approaching_projects
        context['user'] = self.request.user
        context['pending_tasks'] = pending_tasks
        context['recently_completed_tasks'] = Task.objects.all()[:5]
        context['form'] = AddTaskForm(initial={
            'task_owner': self.request.user,
            'task_asignee': self.request.user,
            })
        today = datetime.date.today()
        context['report_day'] = today - datetime.timedelta(today.weekday()) + datetime.timedelta(days=3)
        context['weekly_report'] = Report.objects.filter(report_issued_date__gt=today - datetime.timedelta(today.weekday()))
        return context

# Graph views

# Doughnut chart showing user activity

def user_tasks_chart(request):
    data = []
    labels = []
    late = 0
    close_due = 0
    far_due = 0
    user_tasks = Task.objects.filter(task_asignee__username=request.user.username)
    for task in user_tasks:
        if task.task_status == 'Pending':
            if task.task_due_date < datetime.date.today():
                late = late + 1
            elif task.task_due_date >= datetime.date.today() and \
                task.task_due_date < datetime.date.today() + datetime.timedelta(days=5):
                close_due = close_due + 1
            else:
                far_due = far_due + 1
    labels = ['Late','Approaching','Distant']
    data = [late,close_due,far_due]
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })

# Horizontal bar graph showing team activity per project category

def team_tasks_category(request):
    labels = []
    data = []
    queryset = ProjectCategory.objects\
    .filter(category_projects__project_tasks__task_status='Pending')\
    .annotate(num_tasks=Count('category_projects__project_tasks'))
    for projectcategory in queryset:
        if projectcategory.num_tasks:
            labels.append(projectcategory.projectcategory_name)
            data.append(projectcategory.num_tasks)
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })


# Add Task from Index CRUD

class add_task_index(generic.CreateView):
    model = Task
    fields = ('task_project','task_description',
        'task_owner','task_asignee','task_due_date')
    def get_initial(self):
        return { 'task_owner': self.request.user.pk}
    def get_form(self):
        form = super().get_form()
        return form
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = User.objects.get(id=self.kwargs['pk'])
        return context
    template_name = 'add_task_index.html'
    def get_success_url(self):
        return reverse('index')

# Search bar

class projectsearch(ListView):
    model = Project
    template_name = 'search.html'
    def get_queryset(self, *args, **kwargs):
        val = self.request.GET.get("q")
        if val:
            queryset1 = Project.objects.filter(Q(project_name__icontains=val) | Q(project_number__icontains=val))
            queryset1 = queryset1.distinct()
            queryset2 = Task.objects.filter(Q(task_description__icontains=val) | Q(task_project__project_name__icontains=val))
            queryset2 = queryset2.distinct()
            queryset3 = Subcontractor.objects.filter(Q(subcontractor_name__icontains=val) | Q(subcontractor_job_category__jobcategory_name__icontains=val))
            queryset3 = queryset3.distinct()
            queryset = list(chain(queryset1,queryset2,queryset3))
        else:
            queryset = Project.objects.none()
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['val'] = self.request.GET.get("q")
        return context

def search_autocomplete(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        projects = Project.objects.filter(Q(project_number__icontains=q) | Q(project_name__icontains=q))
        results = []
        for p in projects:
            place_json = p.project_name
            results.append(place_json)
        data = json.dumps(results)
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

# Mark task as complete

def update_task_status(request,pk):
    task = Task.objects.get(pk=pk)
    if task.task_status == 'Pending':
        task.task_status = 'Completed'
        task.task_completion_date = datetime.datetime.now()
        task.save()
    else:
        task.task_status == 'Pending'
        task.task_completion_date = None
        task.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
