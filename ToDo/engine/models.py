from django.db import models

from django.shortcuts import reverse

from django.conf import settings


def files_path_user(instance, filename):
	return f'user_{instance.user.id}/{filename}'


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
	files = models.ManyToManyField("File", blank = True, verbose_name='Файлы')

	def get_absolute_url(self):
		return reverse('detail_note', kwargs = {'pk': self.pk})

	def __str__(self):
		return f"title: {self.title} - id: {self.id}"


class Category(models.Model):
	id = models.BigAutoField(primary_key = True)
	title = models.CharField(max_length = 255, verbose_name = "Название")
	slug = models.SlugField(max_length = 64, unique = True)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)

	def get_absolute_url(self):
		return reverse('detail_category', kwargs = {'slug': self.slug})

	def __str__(self):
	   return f"{self.title}"


class File(models.Model):
	id = models.BigAutoField(primary_key = True)
	file = models.FileField(blank = True, null = True, upload_to = files_path_user, verbose_name = "Файл")
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)

	class Meta:
		verbose_name = "Файлы"
		verbose_name_plural = "Файлы"

	def __str__(self):
		return f"id: {self.id}"
