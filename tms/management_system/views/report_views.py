import json

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from ..forms import ReportCreateForm
from ..models import Report, TP, TCinTP, CustomUser


class ReportView(ListView):
    model = Report
    template_name = 'management_system/reports/report_list.html'
    context_object_name = 'reports'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if context['object_list']:
            for obj in context['object_list']:
                obj.creation_date = str(obj.creation_date.date())
        return context


class ReportCreateView(CreateView):
    model = Report
    form_class = ReportCreateForm
    template_name = 'management_system/reports/report_form.html'
    context_object_name = 'report'

    def get_success_url(self):
        return reverse_lazy('reports')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_id"] = self.request.user.id
        context["structure"] = []
        cleaned_data = kwargs["form"].cleaned_data if "form" in kwargs else None
        if cleaned_data:
            context["name"] = cleaned_data['name'] if "name" in cleaned_data else ""
            context["desc"] = cleaned_data['desc'] if "desc" in cleaned_data else ""
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        plan = get_object_or_404(TP, id=form.data['plan_id'])
        form.instance.plan = plan
        form.save()
        return super(ReportCreateView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return self.render_to_response(self.get_context_data(form=form))


def delete_report(request, pk):
    if request.method == "POST":
        Report.objects.filter(id=pk).delete()
        return redirect('reports')


def report_detail(request, pk):
    report = get_object_or_404(Report, id=pk)
    in_progress = TCinTP.objects.filter(plan_id=report.plan_id, tc_status="IN PROGRESS").count()
    succeed = TCinTP.objects.filter(plan_id=report.plan_id, tc_status="SUCCEED").count()
    failed = TCinTP.objects.filter(plan_id=report.plan_id, tc_status="FAILED").count()
    skipped = TCinTP.objects.filter(plan_id=report.plan_id, tc_status="SKIPPED").count()
    datapoints = [
        {"label": "IN PROGRESS", "y": in_progress},
        {"label": "SUCCEED", "y": succeed},
        {"label": "FAILED", "y": failed},
        {"label": "SKIPPED", "y": skipped}
    ]
    assignee_results = []
    assignees = TCinTP.objects.filter(plan_id=report.plan_id).distinct('assignee_id')
    for a in assignees:
        row = {"y": TCinTP.objects.filter(plan_id=report.plan_id, assignee_id=a.assignee_id).count(),
               "label": get_object_or_404(CustomUser, id=a.assignee_id).username}
        assignee_results.append(row)
    return render(request,
                  'management_system/reports/report_detail.html',
                  {"datapoints": datapoints,
                   "assignee_results": assignee_results})


def get_list_of_plans(request):
    raw_plans = list(TP.objects.all())
    mapped_plans = map(lambda item: {"id": item.id, "name": item.name}, raw_plans)
    return HttpResponse(json.dumps(list(mapped_plans)))
