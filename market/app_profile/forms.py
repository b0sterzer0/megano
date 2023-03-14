from django import forms
from app_login.models import Profile


class ProfileForm(forms.Form):

    avatar = forms.ImageField(required=False)
    full_user_name = forms.CharField(required=False)
    new_email = forms.EmailField(required=False)
    new_phone = forms.CharField(required=False)
    first_new_password = forms.CharField(widget=forms.PasswordInput, required=False)
    second_new_password = forms.CharField(widget=forms.PasswordInput, required=False)

    # class Meta:
    #     model = Profile
    #     # fields = '__all__'
    #     fields = ('avatar',)
    #               'full_user_name',
    #               'new_email',
    #               'new_phone',
    #               'first_new_password',
    #               'second_new_password'
    #               )