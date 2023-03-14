from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy
from django.views.generic import TemplateView

from . import views
from .forms import UserLoginForm, UserPasswordResetForm, SetUserPasswordForm

app_name = 'account'

urlpatterns = [
    path('register/', views.account_register, name='register'),
    path('activate/<slug:uidb64>/<slug:token>/', views.account_activate, name='activate'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='account/registration/login.html',
                                                form_class=UserLoginForm), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('profile/edit/', views.edit_details, name='edit'),
    path('profile/password/', views.UserPasswordChangeView.as_view(), name='password'),
    path('delete/', views.delete_user, name='delete'),
    path('password_reset/', views.UserPasswordResetView.as_view(), name='password_reset'),
    path('reset/sent_mail', TemplateView.as_view(template_name='account/user/password_reset_email_sent.html'),
         name='reset_password_sent'),
    path('password_reset_confirm/<uidb64>/<token>', views.UserPasswordResetConfirm.as_view(),
         name='reset_password_confirm'),
    path('reset/complete/', TemplateView.as_view(template_name='account/user/password_reset_complete.html'), name='password_reset_complete'),

]
