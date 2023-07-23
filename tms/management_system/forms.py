from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import PasswordInput, EmailInput

from .models import CustomUser


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
