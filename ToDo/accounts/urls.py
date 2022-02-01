from django.urls import path

from .views import 	(
    UserCreateView, LoginUser, UserDetailView,
	UserUpdateView, PasswordConfirmView, UserDeleteView,
	logout_user
)


urlpatterns = [
	path('login/', LoginUser.as_view(), name = 'login_user'),
	path('register/', UserCreateView.as_view(), name = 'register_user'),
	path('logout/', logout_user, name = 'logout_user'),
	path("profile/", UserDetailView.as_view(), name = "profile_user"),
	path('profile/edit/', UserUpdateView.as_view(), name = 'edit_user'),
	path('profile/pass_conf/', PasswordConfirmView.as_view(), name = 'password_confirm'),
	path('profile/delete/', UserDeleteView.as_view(), name = 'delete_user'),
]
