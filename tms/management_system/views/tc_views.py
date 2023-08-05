from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from ..forms import TestCaseCreateForm
from ..models import CustomUser, Project, TC, TCHistory, Suit


class TestCaseView(ListView):
    model = TC
    template_name = 'management_system/test_cases/test_cases_list.html'
    context_object_name = 'test_cases'

    def get_queryset(self):
        self.proj_id = get_object_or_404(Project, id=self.kwargs['proj_id'])
        self.suit_id = get_object_or_404(Suit, id=self.kwargs['suit_id'])
        return TC.objects.filter(suit_id=self.suit_id).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_id"] = self.request.user.id
        project = get_object_or_404(Project, id=self.kwargs['proj_id'])
        suit = get_object_or_404(Suit, id=self.kwargs['suit_id'])
        context['modified_users'] = []
        for test_case in context['test_cases']:
            test_case.modified_by = get_object_or_404(CustomUser, id=test_case.modified_by).username
        context["proj_id"] = project.id or None
        context["suit_id"] = suit.id or None
        context["suit_name"] = suit.name or None
        return context


class TestCaseCreateView(CreateView):
    model = TC
    form_class = TestCaseCreateForm
    template_name = 'management_system/test_cases/test_cases_form.html'

    def get_success_url(self):
        return reverse_lazy('test_cases', kwargs={'proj_id': self.kwargs['proj_id'], 'suit_id': self.kwargs['suit_id']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_id"] = self.request.user.id
        context["proj_id"] = get_object_or_404(Project, id=self.kwargs['proj_id']).id
        context["suit_id"] = get_object_or_404(Suit, id=self.kwargs['suit_id']).id
        context["steps"] = [{"index": 0, "step_name": "Step name", "step_value": "Expected result"}]
        cleaned_data = kwargs["form"].cleaned_data if "form" in kwargs else None
        if cleaned_data:
            context["name"] = cleaned_data['name'] if "name" in cleaned_data else ""
            context["desc"] = cleaned_data['desc'] if "desc" in cleaned_data else ""
            context["steps"] = cleaned_data['steps'] if "steps" in cleaned_data else ""
            context["status"] = cleaned_data['status'] if "status" in cleaned_data else "DRAFT"
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.modified_by = self.request.user.id
        project = get_object_or_404(Project, id=self.kwargs['proj_id'])
        form.instance.proj = project
        suit = get_object_or_404(Suit, id=self.kwargs['suit_id'])
        form.instance.suit = suit
        form.save()
        name = form.instance.name
        desc = form.instance.desc
        modified_by = form.instance.modified_by
        status = form.instance.status
        steps = form.instance.steps
        creation_date = form.instance.creation_date
        modification_date = form.instance.modification_date
        proj_id = form.instance.proj_id
        suit_id = form.instance.suit_id
        tc_id = form.instance.id
        user_id = form.instance.user_id
        TCHistory.objects.create(name=name,
                                 desc=desc,
                                 modified_by=modified_by,
                                 status=status,
                                 steps=steps,
                                 creation_date=creation_date,
                                 modification_date=modification_date,
                                 proj_id=proj_id,
                                 suit_id=suit_id,
                                 tc_id=tc_id,
                                 user_id=user_id)
        return super(TestCaseCreateView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return self.render_to_response(self.get_context_data(form=form))


class TestCaseUpdate(UpdateView):
    model = TC
    form_class = TestCaseCreateForm
    template_name = 'management_system/test_cases/test_cases_form.html'

    def get_success_url(self):
        return reverse_lazy('test_cases', kwargs={'proj_id': self.kwargs['proj_id'], 'suit_id': self.kwargs['suit_id']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_id"] = self.request.user.id
        context["proj_id"] = get_object_or_404(Project, id=self.kwargs['proj_id']).id
        context["suit_id"] = get_object_or_404(Suit, id=self.kwargs['suit_id']).id
        tc = get_object_or_404(TC, id=self.kwargs['pk'])
        modified_by_id = get_object_or_404(CustomUser, id=tc.modified_by)
        context["name"] = tc.name
        context["desc"] = tc.desc
        context["steps"] = tc.steps
        context["status"] = tc.status
        context["modified_by"] = modified_by_id
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.modified_by = self.request.user.id
        project = get_object_or_404(Project, id=self.kwargs['proj_id'])
        form.instance.proj = project
        suit = get_object_or_404(Suit, id=self.kwargs['suit_id'])
        form.instance.suit = suit
        form.save()
        name = form.instance.name
        desc = form.instance.desc
        modified_by = form.instance.modified_by
        status = form.instance.status
        steps = form.instance.steps
        creation_date = form.instance.creation_date
        modification_date = form.instance.modification_date
        proj_id = form.instance.proj_id
        suit_id = form.instance.suit_id
        tc_id = form.instance.id
        user_id = form.instance.user_id
        TCHistory.objects.create(name=name,
                                 desc=desc,
                                 modified_by=modified_by,
                                 status=status,
                                 steps=steps,
                                 creation_date=creation_date,
                                 modification_date=modification_date,
                                 proj_id=proj_id,
                                 suit_id=suit_id,
                                 tc_id=tc_id,
                                 user_id=user_id)
        return super(TestCaseUpdate, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return self.render_to_response(self.get_context_data(form=form))


def delete_test_case(request, proj_id, suit_id, pk):
    if request.method == "POST":
        TC.objects.filter(id=pk).delete()
        return redirect('test_cases', proj_id=proj_id, suit_id=suit_id)
