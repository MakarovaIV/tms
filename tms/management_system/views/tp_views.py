import json

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from ..forms import TestPlanCreateForm
from ..models import TP, Project, Suit, CustomUser, TC
from ..models.test_case_in_test_plan import TCinTP


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
        tcases = json.loads(form.data['tc'])
        for tc in tcases:
            TCinTP.objects.create(tc_status=tc['tc_status'],
                                  assignee_id=tc['assignee'],
                                  tc_id=tc['id'],
                                  plan_id=form.instance.id)
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
        tc_in_tp_list = list(TCinTP.objects.filter(plan_id=plan.id))
        structure = []
        for p in projects:
            structure.append({"id": p.id,
                              "name": p.name,
                              "type": "tp-proj",
                              "uniqueId": "proj_" + str(p.id)})
            suits_in_project = list(plan.suit.filter(proj_id=p.id))
            for s in suits_in_project:
                structure.append({"id": s.id,
                                  "name": s.name,
                                  "parentId": "proj_" + str(p.id),
                                  "type": "tp-suit",
                                  "uniqueId": "suit_" + str(s.id)})
                for tc_in_tp in list(filter(lambda it: it.tc.suit_id == s.id, tc_in_tp_list)):
                    structure.append({"id": tc_in_tp.tc.id,
                                      "name": tc_in_tp.tc.name,
                                      "parentId": "suit_" + str(s.id),
                                      "uniqueId": "case_" + str(tc_in_tp.tc.id),
                                      "type": "tp-case",
                                      "assignee": tc_in_tp.assignee,
                                      "tc_status": tc_in_tp.tc_status,
                                      "desc": tc_in_tp.tc.desc})
        context["structure"] = json.dumps(structure)
        context["name"] = plan.name
        context["desc"] = plan.desc
        context["status"] = plan.status
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.modified_by = self.request.user.id
        form.save()
        TCinTP.objects.filter(plan_id=self.kwargs['pk']).delete()
        tcases = json.loads(form.data['tc'])
        existing_items = {}
        for tc in tcases:
            if tc['id'] not in existing_items:
                existing_items[tc['id']] = tc['id']
                TCinTP.objects.create(tc_status=tc['tc_status'],
                                      assignee_id=tc['assignee'],
                                      tc_id=tc['id'],
                                      plan_id=form.instance.id)
        return super(PlanEditView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return self.render_to_response(self.get_context_data(form=form))


def get_projects_to_add(request):
    raw_projects = list(Project.objects.all())
    mapped_projects = map(lambda item: {"id": item.id, "name": item.name}, raw_projects)
    return HttpResponse(json.dumps(list(mapped_projects)))


def get_suits_to_add(request):
    proj_id = request.GET.get('projectid', '')
    mapped_suits = []
    if proj_id:
        raw_suits = list(Suit.objects.filter(proj_id=proj_id))
        mapped_suits = list(map(lambda item: {"id": item.id, "name": item.name, "parentId": item.proj_id}, raw_suits))
    return HttpResponse(json.dumps(mapped_suits))


def get_cases_to_add(request):
    suit_id = request.GET.get('suitid', '')
    mapped_cases = []
    if suit_id:
        raw_suits = list(TC.objects.filter(suit_id=suit_id))
        mapped_cases = list(map(lambda item: {"id": item.id,
                                              "name": item.name,
                                              "desc": item.desc,
                                              "parentId": item.suit_id}, raw_suits))
    return HttpResponse(json.dumps(mapped_cases))
