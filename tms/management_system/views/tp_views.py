import json

from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from ..forms import TestPlanCreateForm
from ..models import TP, Project, Suit, CustomUser, TC


class PlanView(ListView):
    model = TP
    template_name = 'management_system/test_plans/plan_list.html'
    context_object_name = 'plans'

    def get_queryset(self):
        return TP.objects.all().order_by('id')


class PlanCreateView(CreateView):
    model = TP
    form_class = TestPlanCreateForm
    template_name = 'management_system/test_plans/plan_form.html'
    context_object_name = 'plan'

    def get_success_url(self):
        return reverse_lazy('plans')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_id"] = self.request.user.id
        context["modified_by_id"] = self.request.user.id
        context["structure"] = []
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.modified_by = self.request.user.id
        form.save()
        return super(PlanCreateView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors['status'][0])
        return self.render_to_response(self.get_context_data(form=form))


def delete_test_plan(request, pk):
    if request.method == "POST":
        TP.objects.filter(id=pk).delete()
        return redirect('plans')


class PlanEditView(UpdateView):
    model = TP
    form_class = TestPlanCreateForm
    template_name = 'management_system/test_plans/plan_form.html'
    context_object_name = 'plan'

    def get_success_url(self):
        return reverse_lazy('plans')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_id"] = self.request.user.id
        context["modified_by_id"] = self.request.user.id
        plan = get_object_or_404(TP, id=self.kwargs['pk'])
        projects = list(plan.proj.all())
        structure = []
        for p in projects:
            suits_in_project = list(plan.suit.filter(proj_id=p.id))
            suits = []
            for s in suits_in_project:
                cases_in_suit = list(plan.tc.filter(suit_id=s.id, proj_id=p.id))
                cases = []
                for c in cases_in_suit:
                    case = {"id": c.id,
                            "text": c.name,
                            "icon": "fa-regular fa-file",
                            "class": "tp-case"}
                    cases.append(case)
                suit = {"id": s.id,
                        "text": s.name,
                        "icon": "fa-solid fa-list",
                        "class": "tp-suit",
                        "nodes": cases}
                suits.append(suit)
            proj = {"id": p.id,
                    "text": p.name,
                    "icon": "fa-regular fa-folder",
                    "class": "tp-proj",
                    "nodes": suits}
            structure.append(proj)
        context["structure"] = json.dumps(structure)
        context["name"] = plan.name
        context["desc"] = plan.desc
        context["status"] = plan.status
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.modified_by = self.request.user.id
        form.save()
        return super(PlanEditView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return self.render_to_response(self.get_context_data(form=form))