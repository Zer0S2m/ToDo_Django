from datetime import datetime
from datetime import timedelta

from django import forms

from .models import Note
from .models import Category


class NoteForm(forms.ModelForm):
	title = forms.CharField(
		label = "Title",
		required = False,
		widget = forms.TextInput(attrs = {"class": "form-control"}),
		help_text = "Title is not required."
	)
	text = forms.CharField(
		label = "Text", widget = forms.Textarea(attrs = {"class": "form-control", "rows": 5})
	)
	completion_date = forms.DateTimeField(
		label = "Date of completion",
		required = False,
		widget = forms.DateTimeInput(attrs = {"class": "form-control", "type": "date"}),
		help_text = "Date of completion is not required."
	)

	class Meta:
		model = Note
		fields = ("title", "text", "completion_date",)
		widgets = {
			"title": forms.TextInput(attrs = {"class": "form-control"}),
			"text": forms.Textarea(attrs = {"class": "form-control"}),
			"completion_date": forms.DateTimeInput(attrs = {"class": "form-control", "type": "date"}),
		}

	def set_completion_date(self, date: str):
		completion_date_split = list(map(int, date.split("-")))
		completion_date = datetime(*completion_date_split)
		return completion_date

	def clean_completion_date(self):
		completion_date = self.data.get("completion_date")

		if completion_date:
			self.completion_date = self.set_completion_date(completion_date)
			past_date = datetime.now() - timedelta(days = 1)

			if self.completion_date < past_date:
				raise forms.ValidationError(("Completion date cannot be past!"), code = 'past')
			else:
				return completion_date


class CategoryForm(forms.ModelForm):
	title = forms.CharField(
		label = "Title", widget = forms.TextInput(attrs = {"class": "form-control"})
	)

	class Meta:
		model = Category
		fields = ("title",)
		widgets = {
			"title": forms.TextInput(attrs = {"class": "form-control"}),
		}
