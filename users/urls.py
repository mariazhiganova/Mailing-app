from django.contrib.auth.views import LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import RegisterView, UserLoginView, CustomEmailVerificationSentView, CustomPasswordResetView, \
    CustomPasswordResetFromKeyView, CustomPasswordResetDoneView, CustomPasswordResetFromKeyDoneView, \
    CustomPasswordChangeView, BlockedUserView, UserProfileUpdateView, ProfileDetailView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='users:login'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-email-sent/', CustomEmailVerificationSentView.as_view(), name='custom_verify_email_sent'),

    path('password/reset/', CustomPasswordResetView.as_view(), name='account_reset_password'),
    path('password/reset/done/', CustomPasswordResetDoneView.as_view(), name='account_reset_password_done'),
    path('password/reset/key/<uidb36>/<key>/', CustomPasswordResetFromKeyView.as_view(),
         name='account_reset_password_from_key'),
    path('password/reset/key/done/', CustomPasswordResetFromKeyDoneView.as_view(),
         name='account_reset_password_from_key_done'),
    path('password/change/', CustomPasswordChangeView.as_view(), name='account_change_password'),

    path('blocked_page', BlockedUserView.as_view(), name='blocked_page'),

    path('profile/edit/', UserProfileUpdateView.as_view(), name='profile_edit'),
    path('profile/', ProfileDetailView.as_view(), name='profile'),
]
