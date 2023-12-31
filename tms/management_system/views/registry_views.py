import os
import re
import shutil
from pathlib import Path

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect

from ..forms import SignUpForm
from ..models import CustomUser
BASE_DIR = Path(__file__).resolve().parent.parent.parent


def register(request):
    if request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.type = form.cleaned_data['type']
            picture_data = form.cleaned_data['picture']
            default_pic = str(BASE_DIR) + '/icons/user-profile-icon.png'
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
            messages.error(request, form.errors)
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
                return redirect("projects")
            else:
                messages.error(request, 'Login field is empty')
        else:
            messages.error(request, form.errors)
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
