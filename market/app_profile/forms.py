from django import forms


class ProfileForm(forms.Form):

    full_user_name = forms.CharField()
    new_email = forms.EmailField()
    first_new_password = forms.PasswordInput()
    second_new_password = forms.PasswordInput()
