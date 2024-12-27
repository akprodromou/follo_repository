from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from bootstrap_datepicker_plus.widgets import DatePickerInput
from django.views import generic, View
from django.contrib.auth import get_user_model
from django.forms import inlineformset_factory
from reports.models import Report, Action
from .forms import ReportForm, ActionForm
from django.core.exceptions import ValidationError
import datetime
User = get_user_model()


# Reports CRUD

class reports_list(LoginRequiredMixin,generic.ListView):
    model = Report
    template_name = 'report_list.html'

def add_report(request):
    ActionInlineFormSet = inlineformset_factory(
        Report,
        Action,
        form=ActionForm,
        fields=('__all__'),
        extra=1,
        can_delete=False,
        )
    reportform = ReportForm()
    if request.method == "POST":
        reportform = ReportForm(request.POST)
        formset = ActionInlineFormSet(request.POST, instance=reportform.instance)
        if reportform.is_valid():
            reportform.save(commit=False)
            for form in formset:
                if form.has_changed():
                    if form.errors:
                        form_errors = form.errors
                        print(form.errors)
                        return render(request, 'add_report.html',
                            {'formset': formset,
                            'form_errors': form_errors,
                            'reportform':reportform,})
                    else:
                        form.save(commit=False)
            reportform.save()
            for form in formset:
                form.save()
        else:
            reportform_errors = reportform.errors
            print(reportform.errors)
            return render(request, 'add_report.html',
                {'formset': formset,
                'reportform_errors': reportform_errors,
                'reportform':reportform,})
        return redirect(reverse('reports:reports_list'))
    else:
        formset = ActionInlineFormSet()
        reportform = reportform
    return render(request, 'add_report.html', {'formset': formset, 'reportform':reportform,})

def edit_report(request, pk):
    report = Report.objects.get(pk=pk)
    ActionInlineFormSet = inlineformset_factory(
        Report,
        Action,
        form=ActionForm,
        fields=('__all__'),
        extra=1,
        can_delete=False,
        )
    if request.method == "POST":
        reportform = ReportForm(request.POST)
        formset = ActionInlineFormSet(request.POST, instance=report)
        if reportform.is_valid:
            for form in formset:
                if form.has_changed():
                    if form.errors:
                        form_errors = form.errors
                        print(form_errors)
                        return render(request, 'edit_report.html',
                            {'formset': formset,
                            'form_errors': form_errors,
                            'reportform':reportform,})
                    else:
                        form.save()
            return redirect(reverse('reports:reports_list'))
        elif reportform.has_changed() and reportform.errors:
            reportform_errors = reportform.errors
            print(reportform_errors)
            return render(request, 'edit_report.html',
                {'formset': formset,
                'reportform_errors': reportform_errors,
                'reportform':reportform,})
    else:
        formset = ActionInlineFormSet(instance=report)
        reportform = ReportForm(instance=report)
    return render(request, 'edit_report.html', {'formset': formset, 'reportform':reportform,})

class delete_report(LoginRequiredMixin,generic.DeleteView):
    model = Report
    template_name = 'delete_report.html'
    def get_success_url(self):
        return reverse('reports:reports_list')
