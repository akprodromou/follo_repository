from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.utils import timezone
from bootstrap_datepicker_plus.widgets import DatePickerInput
from django.views import generic, View
from django.http import HttpResponseForbidden
from django.views.generic.edit import FormMixin, FormView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import FormView
from braces.views import SelectRelatedMixin
from projects.models import Project
from team.models import Task, Comment, Worktime
from team.forms import CommentForm, AddWorktimeForm
from accounts.forms import *
from django.contrib.auth import get_user_model
from django.db.models.functions import Extract
from django.db.models import Sum, Count
from django.forms.widgets import TextInput, HiddenInput, TimeInput
from django.forms import modelformset_factory, formset_factory
from django.http import JsonResponse
import datetime
User = get_user_model()

# Team VIEWS.PY
# Create your views here.


class users_list(generic.ListView):
    queryset = User.objects.all()
    template_name = 'team/user_list.html'

class user_detail(LoginRequiredMixin,generic.DetailView):
    template_name = 'team/user_detail.html'
    model = User
    context_object_name = 'user_examined'
    def get_success_url(self):
        return reverse('team:user_detail', kwargs={'pk': self.request.user.pk})
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pending_tasks = False
        context["projects_user"] = Project.objects.filter(project_members__id__icontains=self.kwargs['pk'])
        context["user_examined"] = User.objects.get(id=self.kwargs['pk'])
        context["logged_user"] = self.request.user
        # Task context
        user_tasks = Task.objects.filter(task_asignee__id=self.kwargs['pk'])
        context["tasks_all"] = user_tasks
        for task in user_tasks:
            if task.task_status == 'Pending':
                pending_tasks = True
        context["pending_tasks"] = pending_tasks
        try:
            context["completed"] = Task.objects.filter(task_owner__id=self.kwargs['pk']).filter(task_status='Completed').count() / Task.objects.filter(task_owner__id=self.kwargs['pk']).count() * 100
            context["is_due"] = Task.objects.filter(task_owner__id=self.kwargs['pk']).filter(task_status='Pending').count() / Task.objects.filter(task_owner__id=self.kwargs['pk']).count() * 100
            context["tasks"] = Task.objects.filter(task_owner__id=self.kwargs['pk'])
        except:
            context["completed"] = 0
            context["is_due"] = 0
            context["tasks"] = 0
        # Worktime context
        today = datetime.date.today()
        start_of_week_day = today - datetime.timedelta(today.weekday())
        day_difference = datetime.timedelta(days=7)
        mid_date = start_of_week_day + day_difference
        end_date = mid_date + day_difference
        both_dates = [[mid_date, end_date], [start_of_week_day, mid_date]]
        first_week = Worktime.objects.filter(worktime_date__gte=start_of_week_day,
            worktime_date__lt=mid_date).annotate(week=Extract('worktime_date',
            lookup_name='week')).filter(worktime_user__id=self.kwargs['pk'])
        second_week = Worktime.objects.filter(worktime_date__gte=mid_date,
            worktime_date__lt=end_date).annotate(week=Extract('worktime_date',
            lookup_name='week')).filter(worktime_user__id=self.kwargs['pk'])
        both_weeks = [second_week, first_week]
        hours_annotated = Worktime.objects.filter(
            worktime_user__id=self.kwargs['pk'])\
            .filter(worktime_date__gt=start_of_week_day)\
            .annotate(week=Extract('worktime_date',lookup_name='week'))\
            .annotate(year=Extract('worktime_date',lookup_name='year'))\
            .annotate(week_day=Extract('worktime_date',lookup_name='week_day'))
        context['start_date'] = start_of_week_day
        context['mid_date'] = mid_date
        context['end_date'] = end_date
        context['both_weeks'] = zip(both_weeks,both_dates)
        this_year = datetime.datetime.now().year
        context['first_week'] = first_week
        context['hours_annotated'] = hours_annotated
        context["workhours_all"] = Worktime.objects.filter(worktime_user__id=self.kwargs['pk'])\
            .annotate(week=Extract('worktime_date', lookup_name='week'))
        return context

# Task CRUD (user-specific)

class add_task_user(LoginRequiredMixin,generic.CreateView):
    model = Task
    fields = ('task_project','task_description',
        'task_owner','task_asignee','task_due_date')
    def get_initial(self):
        return { 'task_owner': self.kwargs['pk'] }
    def get_form(self):
        form = super().get_form()
        form.fields['task_owner'].widget = HiddenInput()
        form.fields['task_due_date'].widget = DatePickerInput(format='%d/%m/%Y')
        return form
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = User.objects.get(id=self.kwargs['pk'])
        return context
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    template_name = 'team/add_task_user.html'
    def get_success_url(self):
        return reverse('team:user_detail', kwargs={'pk':self.kwargs['pk']})

class edit_task_user(LoginRequiredMixin,generic.UpdateView):
    model = Task
    fields = ('task_project','task_description',
        'task_asignee','task_status','task_due_date')
    def get_form(self):
        form = super().get_form()
        form.fields['task_due_date'].widget = DatePickerInput(format='%d/%m/%Y')
        return form
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = User.objects.get(id=self.object.task_asignee.pk)
        return context
    template_name = 'team/edit_task_user.html'
    def get_success_url(self):
        return reverse('team:user_detail', kwargs={'pk':self.object.task_asignee.pk})

class delete_task_user(LoginRequiredMixin,generic.DeleteView):
    model = Task
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = User.objects.get(id=self.object.task_asignee.pk)
        return context
    template_name = 'team/delete_task_user.html'
    def get_success_url(self):
        return reverse('team:user_detail', kwargs={'pk':self.object.task_asignee.pk})

# Comment CRUD

class AddCommentForm(SingleObjectMixin, FormView):
    template_name = 'team/task_detail.html'
    form_class = CommentForm
    model = Task
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    def get_success_url(self):
        return reverse('team:task_detail', kwargs={'pk': self.object.pk})

# class CommentForm(forms.Form):
#     template_name = 'team/task_detail.html'
#     form_class = CommentForm

class task_display(generic.DetailView):
    model = Task
    def get_success_url(self):
        return reverse('team:task_detail', kwargs={'pk': self.object.pk})
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = Task.objects.get(id=self.kwargs['pk'])
        hours_spent = Worktime.objects.filter(worktime_task=task).aggregate(Sum('worktime_hour'))
        context["form"] = CommentForm(
            initial={
            'comment_author': self.request.user,
            'comment_task': task,
            }
        )
        context["hours_spent"] = hours_spent
        context["task_comments"] = Comment.objects.filter(comment_task__id=self.kwargs['pk'])
        return context
    template_name = 'team/task_detail.html'

class task_detail(View):
    def get(self, request, *args, **kwargs):
        view = task_display.as_view()
        return view(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        view = AddCommentForm.as_view()
        return view(request, *args, **kwargs)

class edit_comment(LoginRequiredMixin,generic.UpdateView):
    model = Comment
    fields = ('comment_text',)
    template_name = 'team/edit_comment.html'
    def get_success_url(self):
        return reverse('team:task_detail', kwargs={'pk':self.kwargs['pk']})

class delete_comment(LoginRequiredMixin,generic.DeleteView):
    model = Comment
    template_name = 'team/delete_comment.html'
    def get_success_url(self):
        return reverse('team:task_detail', kwargs={'pk':self.kwargs['pk']})

# End of comments CRUD

def update_task_status(request,pk):
    task = Task.objects.get(pk=pk)
    if task.task_status == 'Pending':
        task.task_status = 'Completed'
        task.save()
    else:
        task.task_status = 'Pending'
        task.save()
    return redirect('team:user_detail', pk=task.task_owner.pk)

# Worktime CRUD

def add_worktime_user(request, pk):
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
            else:
                form_errors = formset.errors
                return render(request, 'team/add_worktime_user.html', {'formset': formset, 'form_errors': form_errors})
        return redirect(reverse('team:user_detail', kwargs={'pk':pk}))
    else:
        formset = AddWorktimeFormSet(initial=[{'worktime_user': request.user}])
        for form in formset:
            form.fields['worktime_task'].queryset = Task.objects.filter(task_asignee=request.user)
    return render(request, 'team/add_worktime_user.html', {'formset': formset})


class edit_worktime_user(LoginRequiredMixin,generic.UpdateView):
    model = Worktime
    fields = '__all__'
    def get_form(self):
        form = super().get_form()
        form.fields['worktime_date'].widget = DatePickerInput(format='%d/%m/%Y')
        return form
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task_user"] = self.request.user
        return context
    template_name = 'team/edit_worktime_user.html'
    def get_success_url(self):
        return reverse('team:user_detail', kwargs={'pk': self.request.user.pk})

class delete_worktime_user(LoginRequiredMixin,generic.DeleteView):
    model = Worktime
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task_user"] = self.request.user
        return context
    template_name = 'team/delete_worktime_user.html'
    def get_success_url(self):
        return reverse('team:user_detail', kwargs={'pk': self.request.user.pk})

# User worktime history

def first_day_of_week(day_in_data):
    first_day = day_in_data - datetime.timedelta(days=day_in_data.weekday() % 7)
    return first_day

class worktime_list_user(LoginRequiredMixin,generic.ListView):
    model = Worktime
    def get_queryset(self):
        return Worktime.objects.filter(worktime_user__id=self.kwargs['pk'])
    template_name = 'team/worktime_list_user.html'

class worktime_history_user(LoginRequiredMixin,generic.ListView):
    model = Worktime
    def get_queryset(self):
        return Worktime.objects.filter(worktime_user__id=self.kwargs['pk'])
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_examined"] = User.objects.get(id=self.kwargs['pk'])
        return context
    template_name = 'team/worktime_history_user.html'

# User task history

class user_task_history(LoginRequiredMixin,generic.ListView):
    model = Task
    def get_queryset(self):
        return Task.objects.filter(task_owner__id=self.kwargs['pk'])
    template_name = 'team/user_task_history.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = User.objects.get(id=self.kwargs['pk'])
        return context

# Recent team activity

class team_activity(LoginRequiredMixin,generic.ListView):
    model = Task
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        completed_tasks = Task.objects\
        .filter(task_status='Completed')[:25]
        created_tasks = Task.objects.all()\
        .order_by('-task_creation_date')[:25]
        context['combined_list'] = completed_tasks | created_tasks
        return context
    template_name = 'team/team_activity.html'

# User hours per project Graph

def user_hours_graph(request, pk):
    labels = []
    data = []
    reference_date = datetime.date.today() - datetime.timedelta(days=14)
    queryset = Task.objects.filter(task_asignee=pk, task_time__worktime_date__gte=reference_date).\
    annotate(num_hours=Sum('task_time__worktime_hour'))
    for task in queryset:
        if task.num_hours:
            labels.append(task.task_project.project_name)
            data.append(task.num_hours)
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })

# Add worktime from task page

def add_worktime_task(request, pk):
    AddWorktimeFormSet = formset_factory(
        form=AddWorktimeForm,
        extra=0,
        )
    data = request.POST or None
    task_id = pk
    if request.method == 'POST':
        formset = AddWorktimeFormSet(request.POST)
        for form in formset:
            if form.is_valid() and form.has_changed():
                form.save()
            else:
                form_errors = formset.errors
                return render(request, 'team/add_worktime_task.html', {'formset': formset, 'form_errors': form_errors})
        return redirect(reverse('team:task_detail', kwargs={'pk':pk}))
    else:
        formset = AddWorktimeFormSet(initial=[{'worktime_user': request.user, 'worktime_task': Task.objects.get(id=task_id)}])
    return render(request, 'team/add_worktime_task.html', {'formset': formset})
