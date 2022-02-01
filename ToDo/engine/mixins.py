from .models import Category


class MixinNote():
	def get_categories_user(self):
		categories = Category.objects.filter(
			user = self.request.user
		).all()

		return categories
