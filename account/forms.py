from django.db.models import fields

from account.models import User
from django import forms
from django.forms.widgets import Input
from django.contrib.auth.forms import UserCreationForm


class AvatarForm(forms.Form):
    avatar = forms.ImageField(label='')


class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["placeholder"] = "نام کاربری"
        self.fields["first_name"].widget.attrs["placeholder"] = "نام"
        self.fields["last_name"].widget.attrs["placeholder"] = "نام خانوادگی"
        self.fields["email"].widget.attrs["placeholder"] = "ایمیل"
        self.fields["password1"].widget.attrs["placeholder"] = "رمز ورود"
        self.fields["password2"].widget.attrs["placeholder"] = "تکرار رمز ورود"
        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["first_name"].widget.attrs["class"] = "form-control"
        self.fields["last_name"].widget.attrs["class"] = "form-control"
        self.fields["email"].widget.attrs["class"] = "form-control"
        self.fields["password1"].widget.attrs["class"] = "form-control"
        self.fields["password2"].widget.attrs["class"] = "form-control"

    first_name = forms.CharField(
        max_length=30, required=True)
    last_name = forms.CharField(
        max_length=30, required=True)
    email = forms.EmailField(
        max_length=254)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password1', 'password2')
