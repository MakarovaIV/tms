import os
import shutil

from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DetailView
from ..models import CustomUser
from ..forms import CustomUserChangeForm


class UserSettings(UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    success_url = reverse_lazy("projects")

    def post(self, request, *args, **kwargs):
        form = CustomUserChangeForm(request.POST, request.FILES)
        data = request.POST.copy()
        if len(data['username']) > 0:
            is_data_changed = False
            if len(data['username']) > 0:
                if data['username'] != self.request.user.username:
                    self.request.user.username = data['username']
                    is_data_changed = True
            if data['email'] != self.request.user.email:
                self.request.user.email = data['email']
                is_data_changed = True
            if len(data['type']) > 0:
                if data['type'] != self.request.user.type:
                    self.request.user.type = data['type']
                    is_data_changed = True
            picture_data = form.files['picture'] if 'picture' in form.files else None
            if picture_data is not None:
                self.request.user.picture_data = picture_data.file.read()
                is_data_changed = True
            if os.path.exists('tmp_upload'):
                shutil.rmtree('tmp_upload')
            if is_data_changed:
                self.request.user.save()
                messages.info(request, "Changes are saved")
        else:
            messages.error(request, "Incorrect value")
        return render(request, "management_system/customuser_form.html")

    def get(self, request, *args, **kwargs):
        return super().get(self, request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(id=self.request.user.id)


class UserSettingView(DetailView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'management_system/customuser_detail.html'
