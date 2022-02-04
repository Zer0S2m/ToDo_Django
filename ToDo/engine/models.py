from django.db import models

from django.shortcuts import reverse

from django.conf import settings


class Note(models.Model):
	id = models.BigAutoField(primary_key = True)
	title = models.CharField(max_length = 255, blank = True, null = True, verbose_name = "Название")
	text = models.TextField(max_length = 1000, verbose_name = "Описание")
	pub_date = models.DateField(auto_now = True, verbose_name = "Дата публикации")
	category = models.ForeignKey(
		"Category", on_delete = models.SET_NULL, verbose_name = "Категория", blank = True, null = True
	)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
	completion_date = models.DateTimeField(blank = True, null = True, verbose_name = "Дата завершения")

	def get_absolute_url(self):
		return reverse('detail_note', kwargs = {'pk': self.pk})

	def __str__(self):
		return f"{self.title}"


class Category(models.Model):
	id = models.BigAutoField(primary_key = True)
	title = models.CharField(max_length = 255, verbose_name = "Название")
	slug = models.SlugField(max_length = 64, unique = True)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)

	def __str__(self):
	   return f"{self.title}"
