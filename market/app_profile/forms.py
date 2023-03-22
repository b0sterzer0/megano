from django import forms


class ProfileForm(forms.Form):

    avatar = forms.ImageField(required=False)
    full_name = forms.CharField(max_length=200, required=False)
    email = forms.EmailField(required=False)
    phone = forms.CharField(max_length=10, min_length=10, required=False)
    new_password1 = forms.CharField(min_length=8, widget=forms.PasswordInput, required=False)
    new_password2 = forms.CharField(min_length=8, widget=forms.PasswordInput, required=False)
