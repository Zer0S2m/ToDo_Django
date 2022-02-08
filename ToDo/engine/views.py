from datetime import datetime
from distutils.command import upload

from django.shortcuts import render
from django.shortcuts import redirect

from django.http import HttpResponseRedirect

from django.urls import reverse_lazy

from django.db.models import Q

from django.views.generic import (
	ListView, DetailView, DeleteView,
	UpdateView, CreateView
)

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import (
	Note, Category, File
)

from .forms import (
	NoteForm, CategoryForm
)

from .mixins import MixinNote
from .mixins import MixinCategory


def set_date(date: str) -> datetime:
	set_date_split = list(map(int, date.split("-")))
	set_date = datetime(*set_date_split)

	return set_date


def	create_slug_category(title: str, id_user: int) -> str:
	title_split = list(map(lambda char: char.lower(), title.split(" ")))
	slug = "-".join(title_split) + f"_{id_user}"

	return slug


class NoteListView(ListView, MixinNote):
	model = Note
	template_name = "index.html"
	context_object_name = "notes"

	def get_context_data(self, **kwargs):
		self.object_list = []
		context = super().get_context_data(**kwargs)

		if self.request.user.is_authenticated:
			context["notes"] = Note.objects.filter(
				user = self.request.user
			).order_by("-pub_date")
			context["categories"] = self.get_categories_user()

			if len(self.request.GET.get("text_search", "")):
				context = self.found_notes_search_input(context)

			if len(self.request.GET) > 1:
				context = self.found_notes_filter(context)

		return context

	def found_notes_search_input(self, context):
		text_search = self.request.GET.get("text_search", "")

		found_notes = self.model.objects.filter(
			Q(title__icontains = text_search) | Q(text__icontains = text_search),
			user = self.request.user
		).order_by("-pub_date")

		self.object_list = found_notes
		context["notes"] = found_notes
		context["is_search"] = True

		return context

	def found_notes_filter(self, context):
		found_notes = self.model.objects.filter(
			title__icontains = self.request.GET.get("title", ""),
			text__icontains = self.request.GET.get("text", ""),
			user = self.request.user,
		).order_by("-pub_date")

		if self.request.GET.get("date_first", "") and self.request.GET.get("date_second", ""):
			date_first = set_date(date = self.request.GET.get("date_first", ""))
			date_second = set_date(date = self.request.GET.get("date_second", ""))
			min_max_date = sorted([date_first, date_second])

			found_notes = found_notes.filter(
				pub_date__range = (min_max_date[0], min_max_date[1])
			)

		categories = self.request.GET.getlist("category")
		if categories:
			found_notes_category = []
			for category in categories:
				found_notes_category.extend(found_notes.filter(
					category__slug__in = [category]
				))

			found_notes = found_notes_category

		self.object_list = found_notes
		context["notes"] = found_notes
		context["is_search"] = True
		return context


class NoteDetailView(LoginRequiredMixin, DetailView, MixinNote):
	model = Note
	template_name = "detail_note.html"
	context_object_name = "note"

	def get(self, request, *args, **kwargs):
		if not self.check_is_note_user():
			return render(self.request, "404.html", status = 404)

		return super().get(request, *args, **kwargs)


class NoteDeleteView(LoginRequiredMixin, DeleteView, MixinNote):
	model = Note
	template_name = "delete_note.html"
	success_url = reverse_lazy("list_note")

	def get(self, request, *args, **kwargs):
		if not self.check_is_note_user():
			return render(self.request, "404.html", status = 404)

		return super().get(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		object = self.get_object()

		if object.files:
			for file in object.files.all():
				file.delete()

		return super().post(request, *args, **kwargs)


class NoteUpdateView(LoginRequiredMixin, UpdateView, MixinNote):
	model = Note
	template_name = "edit_note.html"
	form_class = NoteForm

	def form_valid(self, form):
		category_id = self.request.POST.get("category")
		object = form.save(commit = False)

		if category_id:
			object.category = Category.objects.filter(
				pk = category_id
			).first()

		object.save()

		return HttpResponseRedirect(self.get_success_url()) 

	def get_success_url(self):
		return self.object.get_absolute_url()

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["categories"] = self.get_categories_user()

		if self.object.completion_date:
			context["due_date"] = self.object.completion_date.strftime("%Y-%m-%d")

		return context

	def get(self, request, *args, **kwargs):
		if not self.check_is_note_user():
			return render(self.request, "404.html", status = 404)

		return super().get(request, *args, **kwargs)


class NoteCreateView(LoginRequiredMixin, CreateView, MixinNote):
	model = Note
	template_name = "create_note.html"
	form_class = NoteForm

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["categories"] = self.get_categories_user()

		return context

	def set_cleaned_data_form(self, form):
		form.cleaned_data["user"] = self.request.user
		category_id = self.request.POST.get("category")

		if category_id:
			form.cleaned_data["category"] = Category.objects.filter(
				pk = int(category_id),
				user = self.request.user
			)

		return form

	def form_valid(self, form):
		files = []
		form = self.set_cleaned_data_form(form)

		self.object = form.save(commit = False)

		self.object.user = form.cleaned_data["user"]
		if "category" in form.cleaned_data:
			self.object.category = form.cleaned_data["category"].first()

		self.object.save()

		if len(self.request.FILES.getlist("files")) > 3:
			form.errors["files"] = "File limit exceeded! Maximum number of files 3!"
			return render(self.request, "create_note.html", {"form": form})

		for file in self.request.FILES.getlist("files"):
			new_file = File(
				file = file,
				user = form.cleaned_data["user"]
			)
			new_file.save()
			files.append(new_file)

		if files:
			self.object.files.add(*files)

		return redirect(self.object)


class CategoryListView(ListView, MixinNote):
	model = Category
	template_name = "list_category.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["count_notes"] = {}

		for category in Category.objects.all():
			context["count_notes"][category.slug] = len(Note.objects.filter(category = category))

		if self.request.user.is_authenticated:
			context["categories"] = self.get_categories_user()

		return context


class CategoryDetailView(LoginRequiredMixin, DetailView, MixinCategory):
	model = Category
	template_name = "detail_category.html"
	context_object_name = "category"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["notes"] = Note.objects.filter(
			category = context["category"]
		)

		return context

	def get(self, request, *args, **kwargs):
		if not self.check_is_category_user():
			return render(self.request, "404.html", status = 404)

		return super().get(request, *args, **kwargs)


class CategoryCreateView(LoginRequiredMixin, CreateView):
	model = Category
	template_name = "create_category.html"
	form_class = CategoryForm

	def set_cleaned_data_form(self, form):
		form.cleaned_data["user"] = self.request.user
		form.cleaned_data["slug"] = create_slug_category(
			title = form.cleaned_data["title"],
			id_user = self.request.user.id
		)

		return form

	def form_valid(self, form):
		form = self.set_cleaned_data_form(form)

		if Category.objects.filter(
			slug = form.cleaned_data["slug"],
			user = self.request.user
		).first():
			form.errors["title"] = "This category already exists!"
			return render(self.request, "create_category.html", {"form": form})

		self.object = form.save(commit = False)
		self.object.user = form.cleaned_data["user"]
		self.object.slug = form.cleaned_data["slug"]

		self.object.save()

		return redirect("list_category")


class CategoryUpdateView(LoginRequiredMixin, UpdateView, MixinCategory):
	model = Category
	template_name = "edit_category.html"
	form_class = CategoryForm

	def get(self, request, *args, **kwargs):
		if not self.check_is_category_user():
			return render(self.request, "404.html", status = 404)

		return super().get(request, *args, **kwargs)

	def get_success_url(self):
		return self.object.get_absolute_url()

	def form_valid(self, form):
		slug = create_slug_category(
			title = form.cleaned_data["title"],
			id_user = self.request.user.id
		)

		if self.kwargs.get(self.slug_url_kwarg) == slug:
			return HttpResponseRedirect(self.get_success_url())

		if self.model.objects.filter(
			slug = slug,
			user = self.request.user
		).first():
			form.errors["title"] = "This category already exists!"
			return render(self.request, "edit_category.html", {"form": form})

		self.object = form.save(commit = False)
		self.object.slug = slug
		self.object.save()

		return HttpResponseRedirect(self.get_success_url())


class CategoryDeleteView(LoginRequiredMixin, DeleteView, MixinCategory):
	model = Category
	template_name = "delete_category.html"
	success_url = reverse_lazy("list_category")

	def get(self, request, *args, **kwargs):
		if not self.check_is_category_user():
			return render(self.request, "404.html", status = 404)

		return super().get(request, *args, **kwargs)
