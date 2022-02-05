from .models import Category


class MixinNote():
	def get_categories_user(self):
		categories = Category.objects.filter(
			user = self.request.user
		)

		return categories

	def check_is_note_user(self):
		if not self.model.objects.filter(
			user = self.request.user,
			pk = self.kwargs.get(self.pk_url_kwarg)
		):
			return False

		return True


class MixinCategory():
	def check_is_category_user(self):
		if not self.model.objects.filter(
			user = self.request.user,
			slug = self.kwargs.get(self.slug_url_kwarg)
		):
			return False

		return True
