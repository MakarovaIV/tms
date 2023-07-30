from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import PasswordInput, EmailInput

from .models import CustomUser, Project, TC, Suit

TC_STATUS = [
    ("ACTIVE", "ACTIVE"),
    ("DRAFT", "DRAFT"),
    ("OUTDATED", "OUTDATED"),
]


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ["username", "email", "picture"]


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ["username", "email", "picture"]


class SignUpForm(UserCreationForm):
    username = forms.CharField(label='Login', max_length=100)
    email = forms.CharField(label='E-mail', widget=EmailInput, required=True)
    password1 = forms.CharField(label='Password', widget=PasswordInput)
    password2 = forms.CharField(label='Repeat Password', widget=PasswordInput)
    picture = forms.FileField(label='Avatar', required=False)

    class Meta:
        model = CustomUser
        fields = ["username", "email", "picture"]

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
    creator_id = forms.IntegerField(required=False)
    modified_by_id = forms.IntegerField(required=False)
    proj_id = forms.IntegerField(required=False)
    suit_id = forms.IntegerField(required=False)
    status = forms.ChoiceField(choices=TC_STATUS)
    steps = forms.JSONField(required=False)

    class Meta:
        model = TC
        fields = ['name',
                  'desc',
                  'creator_id',
                  'modified_by_id',
                  'proj_id',
                  'suit_id',
                  'status',
                  'steps']
