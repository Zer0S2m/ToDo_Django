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

from .models import Note
from .models import Category

from .forms import (
	NoteForm, CategoryForm
)

from .mixins import MixinNote


def	create_slug_category(title: str, id_user: int) -> str:
	title_split = list(map(lambda char: char.lower(), title.split(" ")))
	slug = "-".join(title_split) + f"_{id_user}"

	return slug


class NoteListView(ListView):
	model = Note
	template_name = "index.html"
	context_object_name = "notes"

	def get_context_data(self, **kwargs):
		self.object_list = []
		context = super().get_context_data(**kwargs)

		if self.request.user.is_authenticated:
			context["notes"] = Note.objects.filter(
				user = self.request.user
			).all()

		return context

	def get(self, request, *args, **kwargs):
		text_search = request.GET.get("text_search", "")

		if text_search:
			context = {}
			context = self.found_notes_search_input(text_search, context)

			return self.render_to_response(context)

		return super().get(self, request, *args, **kwargs)

	def found_notes_search_input(self, text_search, context):
		found_notes = self.model.objects.filter(
			Q(title__icontains = text_search) | Q(text__icontains = text_search),
			user = self.request.user
		)

		self.object_list = found_notes
		context["notes"] = found_notes
		context["is_search"] = True

		return context


class NoteDetailView(DetailView):
	model = Note
	template_name = "detail_note.html"
	context_object_name = "note"

	def get(self, request, *args, **kwargs):
		self.object = self.get_object()
		context = self.get_context_data(object = self.object)

		if self.request.user.is_authenticated and self.model.objects.filter(
			id = context["object"].id,
			user = request.user
		).first():
			return self.render_to_response(context)
		else:
			return render(request, "404.html", status = 404)


class NoteDeleteView(DeleteView):
	model = Note
	template_name = "delete_note.html"
	success_url = reverse_lazy("list_note")


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
			).first()

		return form

	def form_valid(self, form):
		form = self.set_cleaned_data_form(form)

		self.object = form.save(commit = False)

		self.object.user = form.cleaned_data["user"]
		if "category" in form.cleaned_data:
			self.object.category = form.cleaned_data["category"]

		self.object.save()

		return redirect(self.object)


class CategoryListView(ListView):
	model = Category
	template_name = "list_category.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["count_notes"] = {}

		for category in Category.objects.all():
			context["count_notes"][category.slug] = len(Note.objects.filter(category = category))

		if self.request.user.is_authenticated:
			context["categories"] = Category.objects.filter(
				user = self.request.user
			).all()

		return context


class CategoryDetailView(DetailView):
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
		self.object = self.get_object()
		context = self.get_context_data(object = self.object)

		if self.request.user.is_authenticated and self.model.objects.filter(
			slug = context["object"].slug,
			user = self.request.user
		).first():
			return self.render_to_response(context)
		else:
			return render(self.request, "404.html", status = 404)


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
				slug = form.cleaned_data["slug"]
			).first():
				form.errors["title"] = "This category already exists!"
				return render(self.request, "create_category.html", {"form": form})

		self.object = form.save(commit = False)
		self.object.user = form.cleaned_data["user"]
		self.object.slug = form.cleaned_data["slug"]

		self.object.save()

		return redirect("list_category")
