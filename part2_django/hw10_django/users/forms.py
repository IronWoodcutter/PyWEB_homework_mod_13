from django.forms import CharField, EmailField, EmailInput, PasswordInput, TextInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class RegisterForm(UserCreationForm):
    username = CharField(max_length=30, required=True, widget=TextInput(attrs={"class": "form-control"}))
    email = EmailField(max_length=50, required=True, widget=EmailInput(attrs={"class": "form-control"}))
    password1 = CharField(min_length=6, max_length=20, required=True,
                          widget=PasswordInput(attrs={"class": "form-control"}))
    password2 = CharField(min_length=6, max_length=20, required=True,
                          widget=PasswordInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class LoginForm(AuthenticationForm):
    username = CharField(max_length=30, required=True, widget=TextInput(attrs={"class": "form-control"}))
    password = CharField(min_length=6, max_length=20, required=True,
                         widget=PasswordInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ("username", "password")
