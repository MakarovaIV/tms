from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from ..forms import ProjectCreateForm
from ..models import Project


class ProjectView(ListView):
    model = Project
    template_name = 'management_system/projects/project_list.html'
    context_object_name = 'projects'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if context['object_list']:
            for obj in context['object_list']:
                obj.creation_date = str(obj.creation_date.date())
        return context


class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectCreateForm
    template_name = 'management_system/projects/project_form.html'
    success_url = reverse_lazy('projects')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_id"] = self.request.user.id
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super(ProjectCreateView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return self.render_to_response(self.get_context_data(form=form))


class ProjectEditView(UpdateView):
    model = Project
    form_class = ProjectCreateForm
    template_name = 'management_system/projects/project_form.html'
    context_object_name = 'project'
    success_url = reverse_lazy('projects')

    def get_queryset(self):
        return Project.objects.filter(id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_id"] = self.request.user.id
        proj = get_object_or_404(Project, id=self.kwargs['pk'])
        context["name"] = proj.name
        context["desc"] = proj.desc
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super(ProjectEditView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return self.render_to_response(self.get_context_data(form=form))


def delete_project(request, pk):
    if request.method == "POST":
        Project.objects.filter(id=pk).delete()
        return redirect('projects')
