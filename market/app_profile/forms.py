from django import forms
from app_login.models import Profile


class ProfileForm(forms.Form):

    avatar = forms.ImageField(required=False)
    full_name = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    phone = forms.CharField(required=False)
    new_password1 = forms.CharField(widget=forms.PasswordInput, required=False)
    new_password2 = forms.CharField(widget=forms.PasswordInput, required=False)
    # new_password1 = forms.PasswordInput()
    # new_password2 = forms.PasswordInput()
