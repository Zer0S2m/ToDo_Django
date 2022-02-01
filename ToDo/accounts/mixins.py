class ProfileMixin():
	def get_object(self):
		return self.model._default_manager.all().filter(
			pk = self.request.user.id
		).get()
