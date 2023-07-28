import os
import re
import shutil

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView

from .forms import SignUpForm, ProjectCreateForm, TestCaseCreateForm
from .models import CustomUser, Project, TC


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


class TestCaseView(ListView):
    model = TC
    template_name = 'management_system/test_cases/test_cases_list.html'
    context_object_name = 'test_cases'

    def get_queryset(self):
        self.proj_id = get_object_or_404(Project, id=self.kwargs['pk'])
        return TC.objects.filter(proj_id=self.proj_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_id"] = self.request.user.id
        project = get_object_or_404(Project, id=self.kwargs['pk'])
        context["proj_id"] = project.id or None
        context["proj_name"] = project.name or None
        return context


class TestCaseCreateView(CreateView):
    model = TC
    form_class = TestCaseCreateForm
    template_name = 'management_system/test_cases/test_cases_form.html'

    def get_success_url(self):
        return reverse_lazy('test_cases', kwargs={'pk': self.kwargs['proj_id']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_id"] = self.request.user.id
        context["proj_id"] = get_object_or_404(Project, id=self.kwargs['proj_id']).id
        context["steps"] = [{"index": 0, "step_name": "Step name", "step_value": "Expected result"}]
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        project = get_object_or_404(Project, id=self.kwargs['pk'])
        form.instance.proj = project
        form.save()
        return super(TestCaseCreateView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Form is invalid")
        return self.render_to_response(self.get_context_data(form=form))


class TestCaseUpdate(UpdateView):
    model = TC
    form_class = TestCaseCreateForm
    template_name = 'management_system/test_cases/test_cases_form.html'

    def get_success_url(self):
        return reverse_lazy('test_cases', kwargs={'pk': self.kwargs['proj_id']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_id"] = self.request.user.id
        context["proj_id"] = get_object_or_404(Project, id=self.kwargs['proj_id']).id
        tc = get_object_or_404(TC, id=self.kwargs['pk'])
        context["name"] = tc.name
        context["desc"] = tc.desc
        context["steps"] = tc.steps
        context["status"] = tc.status

        return context

