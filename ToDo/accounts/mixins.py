from django import forms

from django.contrib.auth.models import User


class ProfileMixin():
	def get_object(self):
		return self.model._default_manager.all().filter(
			pk = self.request.user.id
		).get()


class FormUserMixin():
	def clean_email(self):
		email = self.cleaned_data.get('email')

		if bool(self.instance.username):
			user_email = User.objects.filter(
				email = email,
			).first()
			if user_email and user_email.id == self.instance.id:
				return email
		else:
			user_email = User.objects.filter(
				email = email,
			).first()

		if user_email:
			raise forms.ValidationError(("Email is invalid or already taken!"), code = 'invalid')
	
		return email
