from django.urls import path

from .serializer import ProfileSerializer
from .views import (LoginView, UserRegisterView, EmailConfirmView, NewPasswordSetView, ForgotPasswordView,
                    ForgotPasswordSetView, UserProfileView)


urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user-registration'),
    path('login/', LoginView.as_view(), name='user-login'),
    path('email/confirm/', EmailConfirmView.as_view(), name='email-confirm'),
    path('change/password/<int:id>/', NewPasswordSetView.as_view(), name='password-change'),
    path('forgot/password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('forgot/password/set/', ForgotPasswordSetView.as_view(), name='forgot-password-set'),
    path('profile/', UserProfileView.as_view(), name='request-user-profile')

]