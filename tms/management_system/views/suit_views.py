from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from ..forms import SuitCreateForm
from ..models import CustomUser, Project, Suit


class SuitView(ListView):
    model = Suit
    template_name = 'management_system/suits/suit_list.html'
    context_object_name = 'suits'

    def get_queryset(self):
        self.proj_id = get_object_or_404(Project, id=self.kwargs['pk'])
        return Suit.objects.filter(proj_id=self.proj_id).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_id"] = self.request.user.id
        project = get_object_or_404(Project, id=self.kwargs['pk'])
        context['modified_users'] = []
        for suit in context['suits']:
            suit.modified_by = get_object_or_404(CustomUser, id=suit.modified_by).username
        context["proj_id"] = project.id or None
        context["proj_name"] = project.name or None
        return context


class SuitCreateView(CreateView):
    model = Suit
    form_class = SuitCreateForm
    template_name = 'management_system/suits/suit_form.html'
    context_object_name = 'suit'

    def get_success_url(self):
        return reverse_lazy('suits', kwargs={'pk': self.kwargs['proj_id']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_id"] = self.request.user.id
        proj = get_object_or_404(Project, id=self.kwargs['proj_id'])
        context["proj_id"] = proj.id
        context["proj_name"] = proj.name or None
        cleaned_data = kwargs["form"].cleaned_data if "form" in kwargs else None
        if cleaned_data:
            context["name"] = cleaned_data['name'] if "name" in cleaned_data else ""
            context["desc"] = cleaned_data['desc'] if "desc" in cleaned_data else ""
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.modified_by = self.request.user.id
        project = get_object_or_404(Project, id=self.kwargs['proj_id'])
        form.instance.proj = project
        form.save()
        return super(SuitCreateView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return self.render_to_response(self.get_context_data(form=form))


class SuitEditView(UpdateView):
    model = Suit
    form_class = SuitCreateForm
    template_name = 'management_system/suits/suit_form.html'
    context_object_name = 'suit'
    success_url = reverse_lazy('suits')

    def get_success_url(self):
        return reverse_lazy('suits', kwargs={'pk': self.kwargs['proj_id']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_id"] = self.request.user.id
        context["proj_id"] = get_object_or_404(Project, id=self.kwargs['proj_id']).id
        suit = get_object_or_404(Suit, id=self.kwargs['pk'])
        modified_by_id = get_object_or_404(CustomUser, id=suit.modified_by)
        context["name"] = suit.name
        context["desc"] = suit.desc
        context["modified_by"] = modified_by_id
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.modified_by = self.request.user.id
        project = get_object_or_404(Project, id=self.kwargs['proj_id'])
        form.instance.proj = project
        form.save()
        return super(SuitEditView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return self.render_to_response(self.get_context_data(form=form))


def delete_suit(request, proj_id, pk):
    if request.method == "POST":
        Suit.objects.filter(id=pk).delete()
        return redirect('suits', pk=proj_id)
