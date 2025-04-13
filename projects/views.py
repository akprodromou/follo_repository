from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.views import generic
from django.db.models import Case, CharField, Value, When
from django.db import IntegrityError
from django.utils.decorators import method_decorator
from bootstrap_datepicker_plus import DatePickerInput
from projects.forms import ProjectForm
from team.forms import AddWorktimeForm
from django.forms import MultipleChoiceField
from projects.models import *
from team.models import Task, Worktime
from subcontractors.models import Job
from projects import *
from django.db.models import Count, Sum
from django.http import JsonResponse, HttpResponseRedirect
from django.forms.widgets import HiddenInput
from django.forms import formset_factory
import datetime
User = get_user_model()

# Projects VIEWS.PY file
# Create your views here.

class add_project_category(LoginRequiredMixin,generic.CreateView):
# class add_project_category(generic.CreateView):
    fields = ('projectcategory_number','projectcategory_name')
    model = ProjectCategory
    template_name = 'projects/add_project_category.html'

class add_project(LoginRequiredMixin,generic.CreateView):
# class add_project(generic.CreateView):
    model = Project
    form_class = ProjectForm
    def get_initial (self):
        initial = super().get_initial()
        initial['project_category'] = ProjectCategory.objects.get(projectcategory_number=self.kwargs['pk'])
        initial['project_creator'] = self.request.user
        return initial
    def get_form(self):
        form = super().get_form()
        form.fields['project_delivery_date'].widget = DatePickerInput(format='%d/%m/%Y')
        form.fields['project_creator'].widget = HiddenInput()
        form.fields['project_status'].widget = HiddenInput()
        return form
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["projectcategory"] = ProjectCategory.objects.get(projectcategory_number=self.kwargs['pk'])
        return context
    template_name = 'projects/add_project.html'
    def get_success_url(self):
        return reverse('projects:project_detail', args=[self.object.pk])
        # return reverse('projects:project_detail', kwargs={'<int:pk>': self.object.pk})

class edit_project(LoginRequiredMixin,generic.UpdateView):
# class edit_project(generic.UpdateView):
    model = Project
    form_class = ProjectForm
    def get_form(self):
        form = super().get_form()
        form.fields['project_delivery_date'].widget = DatePickerInput(format='%d/%m/%Y')
        form.fields['project_creator'].widget = HiddenInput()
        form.fields['project_status'].widget = HiddenInput()
        return form
    template_name = 'projects/edit_project.html'
    def get_success_url(self):
        return reverse('projects:project_detail', args=[self.object.pk])

today = datetime.date.today()
start_of_query = today - datetime.timedelta(days=1)
queryset = Project.objects.annotate(num_worktime=Sum('project_tasks__task_time__worktime_hour')).filter(project_tasks__task_time__worktime_date__gte=start_of_query)


class project_categories_list(LoginRequiredMixin,generic.ListView):
# class project_categories_list(generic.ListView):
    model = ProjectCategory
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = datetime.date.today()
        start_of_query = today - datetime.timedelta(days=14)
        context["project_hours_2weeks"] = Project.objects.filter(project_tasks__task_time__worktime_date__gte=start_of_query)
        context["user"] = self.request.user
        return context
    template_name = 'projects/project_categories_list.html'

class project_category(generic.ListView):
    # only projects belonging to a certainn category
    model = Project
    def get_queryset(self):
        return Project.objects.filter(project_category__projectcategory_number=self.kwargs['projectcategory_number'])
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        projectcategory = ProjectCategory.objects.filter(projectcategory_number=self.kwargs['projectcategory_number'])
        context["project_category"] = ProjectCategory.objects.get(projectcategory_number=self.kwargs['projectcategory_number'])
        return context
    template_name = 'projects/project_category.html'

class project_detail(LoginRequiredMixin,generic.DetailView):
# class project_detail(generic.DetailView):
    model = Project
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        project = Project.objects.filter(id=self.kwargs['pk'])
        project_tasks = Task.objects.filter(task_project__id=self.kwargs['pk'])
        pending_tasks = False
        for task in project_tasks:
            if task.task_status == 'Pending':
                pending_tasks = True
        try:
            context["completed"] = Task.objects.filter(task_project__id=self.kwargs['pk']).filter(task_status='Completed').count() / Task.objects.filter(task_project__id=self.kwargs['pk']).count() * 100
            context["is_due"] = Task.objects.filter(task_project__id=self.kwargs['pk']).filter(task_status='Pending').count() / Task.objects.filter(task_project__id=self.kwargs['pk']).count() * 100
            context["tasks"] = Task.objects.filter(task_project__id=self.kwargs['pk'])
        except:
            context["completed"] = 0
            context["is_due"] = 0
            context["tasks"] = 0
        context['tasks_all'] = project_tasks
        context['user'] = self.request.user
        context['jobs'] = Job.objects.filter(job_project__id=self.kwargs['pk'])
        context['pending_tasks'] = pending_tasks
        context['project_tasks'] = project_tasks
        context["workhours_all"] = Worktime.objects.filter(worktime_task__task_project_id=self.kwargs['pk'])
        AddWorktimeFormSet = formset_factory(
            form=AddWorktimeForm,
            extra=0,
            )
        formset = AddWorktimeFormSet(initial=[{'worktime_user': self.request.user}])
        for form in formset:
            form.fields['worktime_task'].queryset = Task.objects.filter(task_asignee=self.request.user,\
            task_project_id=self.kwargs['pk'])
        context['formset'] = formset
        return context
    template_name = 'projects/project_detail.html'

class join_project(LoginRequiredMixin,generic.RedirectView):
# class join_project(generic.RedirectView):
    def get(self,request,*args,**kwargs):
        active_user = self.request.user
        project = get_object_or_404(Project,pk=self.kwargs.get('pk'))
        try:
            project.project_members.add(active_user.pk)
        except IntegrityError:
            messages.warning(self.request,'You have already joined this project')
        else:
            messages.success(self.request,'You have now joined this project!')
        return super().get(request,*args,**kwargs)
    def get_redirect_url(self,*args,**kwargs):
        return reverse('projects:project_detail',kwargs={'pk':self.kwargs.get('pk')})

class leave_project(LoginRequiredMixin,generic.RedirectView):
# class leave_project(generic.RedirectView):
    def get(self,request,*args,**kwargs):
        active_user = self.request.user
        project = get_object_or_404(Project,pk=self.kwargs.get('pk'))
        try:
            member = project.project_members.filter(pk=active_user.pk).get()
        except project.project_members.DoesNotExist:
            messages.warning(self.request,"You can't leave this project because you aren't in it.")
        else:
            project.project_members.remove(active_user.pk)
            messages.success(self.request,"You have successfully left this project.")
        return super().get(request,*args,**kwargs)
    def get_redirect_url(self,*args,**kwargs):
        return reverse('projects:project_detail',kwargs={'pk':self.kwargs.get('pk')})

class add_job_project(LoginRequiredMixin,generic.edit.CreateView):
# class add_job_project(generic.edit.CreateView):
    model = Job
    fields = ('job_description','job_subcontractor',
    'job_project','job_category','job_status',
    'job_requested_date','job_cost')
    def get_initial (self):
        initial = super().get_initial()
        initial['job_project'] = Project.objects.get(id=self.kwargs['pk'])
        return initial
    def get_form(self):
         form = super().get_form()
         form.fields['job_requested_date'].widget = DatePickerInput(format='%d/%m/%Y')
         return form
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["project"] = Project.objects.get(id=self.kwargs['pk'])
        return context
    template_name = 'projects/add_job_project.html'
    def get_success_url(self):
        return reverse('projects:project_detail', args=[self.object.job_project.pk])

# Project Task CRUD

class add_task_project(LoginRequiredMixin,generic.CreateView):
# class add_task_project(generic.CreateView):
    model = Task
    fields = ('task_project','task_description',
        'task_owner','task_asignee','task_due_date')
    def get_initial(self):
        return {
        'task_project': self.kwargs['pk'],
        'task_owner': self.request.user,
        'task_asignee': self.request.user
        }
    def get_form(self):
        form = super().get_form()
        form.fields['task_owner'].widget = HiddenInput()
        form.fields['task_due_date'].widget = DatePickerInput(format='%d/%m/%Y')
        return form
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["project"] = Project.objects.get(id=self.kwargs['pk'])
        return context
    template_name = 'projects/add_task_project.html'
    def get_success_url(self):
        return reverse('projects:project_detail', kwargs={'pk': self.kwargs['pk']})


# Project task history

class project_task_history(generic.ListView):
    model = Task
    def get_queryset(self):
        return Task.objects.filter(task_project__id=self.kwargs['pk'])
    template_name = 'projects/project_task_history.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["project"] = Project.objects.get(id=self.kwargs['pk'])
        return context

# Graph showing workhours per project

def busiest_projects(request):
    labels = []
    data = []
    today = datetime.date.today()
    start_of_query = today - datetime.timedelta(days=14)
    queryset = Project.objects\
        .filter(project_tasks__task_time__worktime_date__gte=start_of_query)\
        .annotate(num_worktime=Sum('project_tasks__task_time__worktime_hour'))
    for project in queryset:
        if project.num_worktime:
            labels.append(project.project_name)
            data.append(project.num_worktime)
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })

# Graph showing workhours per project category

def busiest_project_categories(request):
    labels = []
    data = []
    today = datetime.date.today()
    start_of_query = today - datetime.timedelta(days=14)
    queryset = ProjectCategory.objects\
    .filter(category_projects__project_tasks__task_time__worktime_date__gte=start_of_query)\
    .annotate(num_worktime=Sum('category_projects__project_tasks__task_time__worktime_hour'))
    for projectcategory in queryset:
        if projectcategory.num_worktime:
            labels.append(projectcategory.projectcategory_name)
            data.append(projectcategory.num_worktime)
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })

# Project hours per user graph

def project_hours_graph(request, pk):
    labels = []
    data = []
    queryset = Worktime.objects.\
    values('worktime_user__username').\
    filter(worktime_task__task_project_id=pk).\
    annotate(hours_sum=Sum('worktime_hour'))
    for dict in queryset:
        labels.append(dict['worktime_user__username'])
        data.append(dict['hours_sum'])
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })

# Add worktime from project page
# NOT IN USE

def add_worktime_project(request, pk):
    AddWorktimeFormSet = formset_factory(
        form=AddWorktimeForm,
        extra=0,
        )
    data = request.POST or None
    user_id = pk
    if request.method == 'POST':
        formset = AddWorktimeFormSet(request.POST)
        for form in formset:
            if form.is_valid() and form.has_changed():
                form.save()
        return redirect(reverse('projects:project_detail', kwargs={'pk':pk}))
    else:
        formset = AddWorktimeFormSet(initial=[{'worktime_user': request.user}])
        for form in formset:
            form.fields['worktime_task'].queryset = Task.objects.filter(task_asignee=request.user, task_project_id=pk)
    return render(request, 'projects/add_worktime_project.html', {'formset': formset})

# Add worktime modal

def add_worktime_modal(request, pk):
    AddWorktimeFormSet = formset_factory(
        form=AddWorktimeForm,
        extra=0,
        )
    data = request.POST or None
    if request.method == 'POST':
        formset = AddWorktimeFormSet(request.POST)
        for form in formset:
            if form.is_valid() and form.has_changed():
                form.save()
        return redirect(reverse('projects:project_detail', kwargs={'pk':pk}))
    else:
        formset = AddWorktimeFormSet(initial=[{'worktime_user': request.user}])
        for form in formset:
            form.fields['worktime_task'].queryset = Task.objects.filter(task_asignee=request.user)
    return render('projects:add_worktime_modal')
