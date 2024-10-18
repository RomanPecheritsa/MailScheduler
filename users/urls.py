from django.contrib.auth.views import LogoutView, PasswordChangeView
from django.urls import path

from users.views import UserLoginView, UserCreateView, email_verification

app_name = 'users'

urlpatterns = [
    path('login/', UserLoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', UserCreateView.as_view(), name='register'),
    path("email-confirm/<str:token>/", email_verification, name="email_confirm"),
]
