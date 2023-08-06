from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import EmailValidationOnForgotPassword

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             form_class=EmailValidationOnForgotPassword,
             template_name='password_reset.html',
             subject_template_name='password_reset_subject.txt',
             html_email_template_name='html_password_reset_email.html'),
         name='password-reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='password_reset_complete.html'
         ),
         name='password_reset_complete')
]