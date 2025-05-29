from django.urls import path
from django.contrib.auth import views as auth_views
from user import views

urlpatterns = [
    path('profile/', views.user_profile, name='profile'),
    path('profile/update/', views.user_update, name='update_profile'),

    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.user_register, name='register'),


    path('password-change/', auth_views.PasswordChangeView.as_view(
        template_name='user/password_change.html'), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='user/password_change_done.html'), name='password_change_done'),
    
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='user/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='user/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='user/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='user/password_reset_complete.html'), name='password_reset_complete'),
]
