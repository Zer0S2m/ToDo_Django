from django import forms

from django.contrib.auth import password_validation
from django.contrib.auth.forms import (
	UserCreationForm, AuthenticationForm
)
from django.contrib.auth.models import User

from django.core.exceptions import ValidationError

from django.utils.translation import gettext_lazy as _

from .mixins import FormUserMixin


class RegisterForm(UserCreationForm, FormUserMixin):
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


class UserForm(forms.ModelForm, FormUserMixin):
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


class ChangePassword(forms.ModelForm):
	error_messages = {
		'password_mismatch': ("Password mismatch!"),
	}

	password1 = forms.CharField(
		label = "Password",
		widget = forms.PasswordInput(attrs = {"class": "form-control"}),
		strip = False,
	)
	password2 = forms.CharField(
		label = "Password confirmation",
		widget = forms.PasswordInput(attrs = {"class": "form-control"}),
		strip = False,
	)

	class Meta:
		model = User
		fields = ("password1", "password2")
		widgets = {
			"password1": forms.PasswordInput(attrs = {"class": "form-control"}),
			"password2": forms.PasswordInput(attrs = {"class": "form-control"}),
		}

	def clean_password2(self):
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')

		if password1 != password2:
			raise forms.ValidationError(
				self.error_messages['password_mismatch'],
				code = 'password_mismatch',
			)

		return password2

	def _post_clean(self):
		super()._post_clean()
		password = self.cleaned_data.get('password2')

		if password:
			try:
				password_validation.validate_password(password, self.instance)
			except ValidationError as error:
				self.add_error('password2', error)
