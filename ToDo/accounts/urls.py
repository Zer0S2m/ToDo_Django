from django.urls import path

from .views import 	(
    UserCreateView, LoginUser, UserDetailView,
	UserUpdateView, PasswordConfirmView, UserDeleteView,
	logout_user, activation_sent, activate_user,
	reset_password, PasswordChange, password_change_done,
	reset_password_done
)


urlpatterns = [
	path('login/', LoginUser.as_view(), name = 'login_user'),
	path('register/', UserCreateView.as_view(), name = 'register_user'),
	path('logout/', logout_user, name = 'logout_user'),

	path('activation_sent/', activation_sent, name = 'activation_sent_email_user'),
	path('activate/<str:uidb64>/<str:token>/', activate_user, name = 'activate_email_user'),

	path('password_reset/', reset_password, name = 'reset_password_user'),
	path('password_reset/done/', reset_password_done, name = 'reset_password_done_user'),
	path("password_change/<str:uidb64>/<str:token>/", PasswordChange.as_view(), name = "change_password_user"),
	path("password_change/done/", password_change_done, name = "change_password_done_user"),

	path("profile/", UserDetailView.as_view(), name = "profile_user"),
	path('profile/edit/', UserUpdateView.as_view(), name = 'edit_user'),
	path('profile/pass_conf/', PasswordConfirmView.as_view(), name = 'password_confirm'),
	path('profile/delete/', UserDeleteView.as_view(), name = 'delete_user'),
]
