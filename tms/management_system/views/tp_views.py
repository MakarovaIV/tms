import json

from django.contrib import messages
from django.http import HttpResponse
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
        messages.error(self.request, form.errors)
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
            button_add_suit = '<button type="button" class="btn btn-info" onclick="addSuitHandler(event,' + str(p.id) + ')">Add suit</button>'
            structure.append({"id": p.id,
                              "name": p.name,
                              "type": "tp-proj",
                              "action": button_add_suit})
            suits_in_project = list(plan.suit.filter(proj_id=p.id))
            for s in suits_in_project:
                button_add_case = '<button type="button" class="btn btn-info" onclick="addCaseHandler(event,' + str(s.id) + ')">Add case</button>'
                structure.append({"id": s.id,
                                  "name": s.name,
                                  "parentId": p.id,
                                  "type": "tp-suit",
                                  "action": button_add_case})
                cases_in_suit = list(plan.tc.filter(suit_id=s.id, proj_id=p.id))
                for c in cases_in_suit:
                    structure.append({"id": c.id,
                                      "text": c.name,
                                      "parentId": s.id,
                                      "type": "tp-case"})
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


def get_projects_to_add(request):
    raw_projects = list(Project.objects.all())
    mapped_projects = map(lambda item: {"id": item.id, "name": item.name}, raw_projects)
    return HttpResponse(json.dumps(list(mapped_projects)))


