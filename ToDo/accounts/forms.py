from django import forms

from django.contrib.auth.forms import (
	UserCreationForm, AuthenticationForm
)
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
	username = forms.CharField(
		label = "Login", widget = forms.TextInput(attrs = {"class": "form-control"})
	)
	password1 = forms.CharField(
		label = "Password", widget = forms.PasswordInput(attrs = {"class": "form-control"})
	)
	password2 = forms.CharField(
		label = "Password confirmation", widget = forms.PasswordInput(attrs = {"class": "form-control"})
	)
	email = forms.EmailField(
		label = "Email", required = True, widget = forms.TextInput(attrs = {"class": "form-control", "type": "email"})
	)

	class Meta:
		model = User
		fields = ("username", "password1", "password2")
		widgets = {
			"username": forms.TextInput(attrs = {"class": "form-control"}),
			"password1": forms.PasswordInput(attrs = {"class": "form-control"}),
			"password2": forms.PasswordInput(attrs = {"class": "form-control"}),
			"email": forms.TextInput(attrs = {"class": "form-control", "type": "email"}),
		}


class LoginUserForm(AuthenticationForm):
	username = forms.CharField(
		label = "Login", widget = forms.TextInput(attrs = {"class": "form-control"})
	)
	password = forms.CharField(
		label = "Password", widget = forms.PasswordInput(attrs = {"class": "form-control"})
	)
	remember_me = forms.BooleanField(
		label = "Remember me", required = False, widget = forms.CheckboxInput(attrs = {"class": "form-check-input"})
	)


class UserForm(forms.ModelForm):
	username = forms.CharField(
		label = "Login", widget = forms.TextInput(attrs = {"class": "form-control"})
	)
	first_name = forms.CharField(
		label = "First name", required = False, widget = forms.TextInput(attrs = {"class": "form-control"})
	)
	last_name = forms.CharField(
		label = "Last name", required = False, widget = forms.TextInput(attrs = {"class": "form-control"})
	)
	email = forms.CharField(
		label = "Email", required = False, widget = forms.TextInput(attrs = {"class": "form-control", "type": "email"})
	)

	class Meta:
		model = User
		fields = ('username', "first_name", "last_name", "email")


class PasswordConfirmForm(forms.ModelForm):
	password = forms.CharField(
		label = "Password", widget = forms.PasswordInput(attrs = {"class": "form-control"})
	)

	class Meta:
		model = User
		fields = ("password",)
