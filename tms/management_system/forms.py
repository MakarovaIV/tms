from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import PasswordInput, EmailInput

from .models import CustomUser, Project, TC, Suit, TP, Report

ROLES = [
    ("Admin", "Admin"),
    ("Owner", "Owner"),
    ("Developer", "Developer"),
    ("Tester", "Tester")
]

TC_STATUS = [
    ("ACTIVE", "ACTIVE"),
    ("DRAFT", "DRAFT"),
    ("OUTDATED", "OUTDATED"),
]

TP_STATUS = [
    ("IN PROGRESS", "IN PROGRESS"),
    ("DONE", "DONE"),
    ("CANCELLED", "CANCELLED"),
]

TC_IN_TP_STATUS = [
    ("IN PROGRESS", "IN PROGRESS"),
    ("SUCCEED", "SUCCEED"),
    ("FAILED", "FAILED"),
    ("SKIPPED", "SKIPPED"),
]


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ["username", "email", "picture", "type"]


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ["username", "email", "picture", "type"]


class SignUpForm(UserCreationForm):
    username = forms.CharField(label='Login', max_length=100)
    email = forms.CharField(label='E-mail', widget=EmailInput, required=True)
    password1 = forms.CharField(label='Password', widget=PasswordInput)
    password2 = forms.CharField(label='Repeat Password', widget=PasswordInput)
    picture = forms.FileField(label='Avatar', required=False)
    type = forms.ChoiceField(label='Role', choices=ROLES)

    class Meta:
        model = CustomUser
        fields = ["username", "email", "picture", "type"]

    def clean_email(self):
        '''
        Verify email is available.
        '''
        email = self.cleaned_data.get('email')
        user_email = CustomUser.objects.filter(email=email)
        if user_email.exists():
            raise forms.ValidationError("Email is existed")
        return email


class ProjectCreateForm(forms.ModelForm):
    name = forms.CharField(max_length=100)
    desc = forms.CharField(widget=forms.Textarea)
    user_id = forms.IntegerField(required=False)

    class Meta:
        model = Project
        fields = ['name',
                  'desc',
                  'user_id']


class SuitCreateForm(forms.ModelForm):
    name = forms.CharField(max_length=100)
    desc = forms.CharField(widget=forms.Textarea)
    user_id = forms.IntegerField(required=False)
    proj_id = forms.IntegerField(required=False)
    modified_by_id = forms.IntegerField(required=False)

    class Meta:
        model = Suit
        fields = ['name',
                  'desc',
                  'user_id',
                  'proj_id',
                  'modified_by_id']


class TestCaseCreateForm(forms.ModelForm):
    name = forms.CharField(max_length=200)
    desc = forms.CharField(widget=forms.Textarea)
    user_id = forms.IntegerField(required=False)
    modified_by_id = forms.IntegerField(required=False)
    proj_id = forms.IntegerField(required=False)
    suit_id = forms.IntegerField(required=False)
    status = forms.ChoiceField(choices=TC_STATUS)
    steps = forms.JSONField(required=False)

    class Meta:
        model = TC
        fields = ['name',
                  'desc',
                  'user_id',
                  'modified_by_id',
                  'proj_id',
                  'suit_id',
                  'status',
                  'steps']


class TestPlanCreateForm(forms.ModelForm):
    name = forms.CharField(max_length=200, error_messages={'required': 'Field name is invalid'})
    desc = forms.CharField(widget=forms.Textarea, error_messages={'required': 'Field desc is invalid'})
    user_id = forms.IntegerField(error_messages={'required': 'Field user_id is invalid'})
    modified_by_id = forms.IntegerField(error_messages={'required': 'Field modified_by_id is invalid'})
    proj = forms.JSONField(error_messages={'required': 'Field proj is invalid'}, required=False)
    suit = forms.JSONField(error_messages={'required': 'Field suit is invalid'}, required=False)
    tc = forms.JSONField(error_messages={'required': 'Field tc is invalid'}, required=False)
    status = forms.ChoiceField(choices=TP_STATUS, error_messages={'required': 'Field status is invalid'}, required=False)

    class Meta:
        model = TP
        fields = ['name',
                  'desc',
                  'user_id',
                  'modified_by_id',
                  'proj',
                  'suit',
                  'tc',
                  'status']


class ReportCreateForm(forms.ModelForm):
    name = forms.CharField(max_length=100)
    user_id = forms.IntegerField(required=False)
    plan_id = forms.IntegerField(required=False)

    class Meta:
        model = Report
        fields = ['name',
                  'user_id',
                  'plan_id']
