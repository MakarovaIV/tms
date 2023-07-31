import os
import re
import shutil

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from .forms import SignUpForm, ProjectCreateForm, TestCaseCreateForm, SuitCreateForm
from .models import CustomUser, Project, TC, TCHistory, Suit


def register(request):
    if request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            picture_data = form.cleaned_data['picture']
            default_pic = 'icons/user-profile-icon.png'
            if picture_data is not None:
                user.picture_data = picture_data.file.read()
            else:
                with open(default_pic, 'rb') as data:
                    user.picture_data = data.read()
            user.save()
            if os.path.exists('tmp_upload'):
                shutil.rmtree('tmp_upload')
            return redirect("login")
    else:
        form = SignUpForm()
    return render(request=request,
                  template_name="management_system/signup_form.html",
                  context={"form": form})


def login_handler(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are logged in as {username}.")
                return redirect("index")
            else:
                messages.error(request, 'Login field is empty')
        else:
            messages.error(request, 'Login or password incorrect')
    form = AuthenticationForm()
    return render(request=request, template_name="management_system/login.html", context={"login_form": form})


def logout_handler(request):
    if request.session:
        logout(request)
    messages.info(request, "Logged out successfully!")
    return render(request=request, template_name="management_system/logout.html")


def get_user_image(request, pk):
    if request.method == "GET":
        data = CustomUser.objects.filter(id=pk)
        picture_data = list(data)[0].picture_data
        matches = re.match(r".+\.(.+)$", str(list(data)[0].picture))
        extension = matches.group(1) if matches else "jpeg"
        content_type = "image/" + extension
        return HttpResponse(picture_data, content_type=content_type)


class ProjectView(ListView):
    model = Project
    template_name = 'management_system/projects/project_list.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return Project.objects.all().order_by('id')


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


def delete_project(request, pk):
    Project.objects.filter(id=pk).delete()
    return redirect('projects')


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
        context["proj_id"] = get_object_or_404(Project, id=self.kwargs['proj_id']).id
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.modified_by = self.request.user.id
        project = get_object_or_404(Project, id=self.kwargs['proj_id'])
        form.instance.proj = project
        form.save()
        return super(SuitCreateView, self).form_valid(form)


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


class SuitDeleteView(DeleteView):
    model = Suit
    template_name = 'management_system/suits/suit_form_delete.html'
    success_url = reverse_lazy('suits')

    def get_success_url(self):
        return reverse_lazy('suits', kwargs={'pk': self.kwargs['proj_id']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_id"] = self.request.user.id
        context["proj_id"] = get_object_or_404(Project, id=self.kwargs['proj_id']).id
        return context


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
        messages.error(self.request, "Form is invalid")
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


class TestCaseDelete(DeleteView):
    model = TC
    template_name = 'management_system/test_cases/test_cases_form_delete.html'

    def get_success_url(self):
        return reverse_lazy('test_cases', kwargs={'proj_id': self.kwargs['proj_id'], 'suit_id': self.kwargs['suit_id']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_id"] = self.request.user.id
        context["proj_id"] = get_object_or_404(Project, id=self.kwargs['proj_id']).id
        context["suit_id"] = get_object_or_404(Suit, id=self.kwargs['suit_id']).id
        return context


class TCHistoryView(ListView):
    model = TCHistory
    template_name = 'management_system/tc_history/tc_history_list.html'
    context_object_name = 'tc_history'

    def get_queryset(self):
        self.proj_id = get_object_or_404(Project, id=self.kwargs['proj_id'])
        self.suit_id = get_object_or_404(Suit, id=self.kwargs['suit_id'])
        self.pk = get_object_or_404(TC, id=self.kwargs['pk'])
        return TCHistory.objects.filter(tc_id=self.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_id"] = self.request.user.id
        context["proj_id"] = get_object_or_404(Project, id=self.kwargs['proj_id']).id
        context["suit_id"] = get_object_or_404(Suit, id=self.kwargs['suit_id']).id
        tc = get_object_or_404(TC, id=self.kwargs['pk'])
        modified_by_id = get_object_or_404(CustomUser, id=tc.modified_by)
        context["tc"] = tc
        context["name"] = tc.name
        context["desc"] = tc.desc
        context["steps"] = tc.steps
        context["status"] = tc.status
        context["modified_by"] = modified_by_id
        return context


class TCHistoryDetailView(DetailView):
    model = TCHistory
    template_name = 'management_system/tc_history/tc_history_detail.html'
    context_object_name = 'tc_history_detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["proj_id"] = get_object_or_404(Project, id=self.kwargs['proj_id']).id
        context["suit_id"] = get_object_or_404(Suit, id=self.kwargs['suit_id']).id
        context["tc"] = get_object_or_404(TC, id=self.object.tc_id)
        return context

    def get_success_url(self):
        return reverse_lazy('tc_history_detail', kwargs={'proj_id': self.kwargs['proj_id'],
                                                         'suit_id': self.kwargs['suit_id'],
                                                         'tc': self.object.tc_id})


def recover_tc(request, proj_id, suit_id, tc_id, pk):
    data = request.POST.copy()
    if request.user.is_authenticated:
        tc = TCHistory.objects.filter(pk=pk).get()
        name = tc.name
        desc = tc.desc
        modified_by = tc.modified_by
        status = tc.status
        steps = tc.steps
        creation_date = tc.creation_date
        modification_date = tc.modification_date
        proj_id = tc.proj_id
        suit_id = tc.suit_id
        user_id = tc.user_id
        TC.objects.filter(pk=tc.tc_id).update(name=name,
                                              desc=desc,
                                              modified_by=modified_by,
                                              status=status,
                                              steps=steps,
                                              creation_date=creation_date,
                                              modification_date=modification_date,
                                              proj_id=proj_id,
                                              suit_id=suit_id,
                                              user_id=user_id)
        # updated_tc.save()
        return redirect('tc_update', proj_id=proj_id, suit_id=suit_id, pk=tc.tc_id)
