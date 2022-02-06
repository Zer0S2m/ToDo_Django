from django.shortcuts import redirect
from django.shortcuts import render

from django.utils.encoding import force_text
from django.utils.encoding import force_bytes

from django.utils.http import urlsafe_base64_decode
from django.utils.http import urlsafe_base64_encode

from django.views.generic import (
	CreateView, View, TemplateView
)
from django.views.generic.base import (
	ContextMixin, TemplateResponseMixin, View
)
from django.views.generic.edit import (
	FormView, UpdateView, DeletionMixin
)

from django.contrib.sites.shortcuts import get_current_site

from django.template.loader import render_to_string

from django.urls import reverse_lazy

from django.contrib.auth import (
	login, logout, authenticate
)
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView

from .forms import (
	RegisterForm, LoginUserForm, UserForm,
	PasswordConfirmForm
)

from .tokens import account_activation_token

from .mixins import ProfileMixin


class UserDetailView(TemplateResponseMixin, ContextMixin, View):
	template_name = "profile.html"

	def get(self, request, *args, **kwargs):
		if not self.request.user.is_authenticated:
			return render(request, "404.html", status = 404)

		context = self.get_context_data(**kwargs)
		return self.render_to_response(context)


class UserCreateView(CreateView):
	form_class = RegisterForm
	template_name = "sign_up.html"
	success_url = reverse_lazy("login_user")

	def form_valid(self, form):
		user = form.save(commit = False)
		user.is_active = False
		user.email = form.cleaned_data["email"]
		user.save()

		current_site = get_current_site(self.request)
		subject = 'Activate Your MySite Account'

		message = render_to_string('activation_sent_email.html', {
			'user': user,
			'domain': current_site.domain,
			'uid': urlsafe_base64_encode(force_bytes(user.pk)),
			'token': account_activation_token.make_token(user),
		})

		user.email_user(subject, message)

		return redirect('activation_sent_email_user')


class LoginUser(LoginView):
	form_class = LoginUserForm
	template_name = "login.html"

	def get_success_url(self):
		return reverse_lazy("list_note")

	def form_valid(self, form):
		remember_me = form.cleaned_data.get('remember_me')

		if not remember_me:
			self.request.session.set_expiry(0)
			self.request.session.modified = True

		return super(LoginUser, self).form_valid(form)


class UserUpdateView(UpdateView):
	model = User
	form_class = UserForm
	template_name = "edit.html"
	success_url = reverse_lazy("profile_user")

	def get(self, request, *args, **kwargs):
		if not self.request.user.is_authenticated:
			return render(self.request, "404.html", status = 404)
		
		self.kwargs = {
			"pk": self.request.user.id
		}

		self.object = self.get_object(
			queryset = self.model.objects.filter(
				pk = self.kwargs.get("pk")
			)
		)

		fields_user = self.return_fields_user()
		context_data = self.get_context_data()

		for field in context_data["form"].fields:
			if fields_user[field]:
				context_data["form"].fields[field].widget.attrs["value"] = fields_user[field]

		return self.render_to_response(context_data)

	def post(self, request, *args, **kwargs):
		self.kwargs = {
			"pk": self.request.user.id
		}
		return super().post(request, *args, **kwargs)

	def form_valid(self, form):
		self.save(form)
		return super().form_valid(form)

	def save(self, form):
		for key, value in form.cleaned_data.items():
			setattr(self.object, key, value)

		self.object.save()

	def return_fields_user(self):
		return {
			"username": self.request.user.username,
			"first_name": self.request.user.first_name,
			"last_name": self.request.user.last_name,
			"email": self.request.user.email,
		}


class UserDeleteView(ProfileMixin, TemplateView, DeletionMixin):
	model = User
	template_name = "delete.html"
	success_url = reverse_lazy("list_note")

	def get(self, request, *args, **kwargs):
		if not request.session.get('is_deleted_user'):
			return redirect("password_confirm")
		
		del request.session["is_deleted_user"]

		return super().get(request, *args, **kwargs)


class PasswordConfirmView(ProfileMixin, FormView):
	model = User
	template_name = "password_confirm.html"
	form_class = PasswordConfirmForm
	success_url = reverse_lazy("delete_user")

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		return super().post(request, *args, **kwargs)

	def form_valid(self, form):
		is_authenticate = authenticate(
			username = self.request.user,
			password = form.cleaned_data["password"]
		)

		if not is_authenticate:
			form.errors["password"] = "Invalid password"
			return self.form_invalid(form)

		self.set_session_deleted_user()

		return super().form_valid(form)

	def set_session_deleted_user(self):
		self.request.session["is_deleted_user"] = True


def	logout_user(request):
	logout(request)
	return redirect("login_user")


def activation_sent(request):
	return render(request, "activate_sent.html")


def activate(request, uidb64, token):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk = uid)
	except (
		TypeError,
		ValueError,
		OverflowError,
		User.DoesNotExist
	):
		user = None

	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		user.save()
		login(request, user)

		return redirect('profile_user')
	else:
		return render(request, 'activate_sent_invalid.html')
