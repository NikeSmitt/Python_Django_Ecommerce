from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetConfirmView, PasswordChangeView
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .forms import RegistrationForm, UserEditForm, UserPasswordResetForm, SetUserPasswordForm, UserPasswordChangeForm
from .models import UserBase
from .token import account_activation_token


def account_register(request):
    # if request.user.is_authenticated:
    #     return redirect('/')
    
    if request.method == 'POST':
        register_form = RegistrationForm(request.POST)
        if register_form.is_valid():
            user = register_form.save(commit=False)
            user.email = register_form.cleaned_data['email']
            user.set_password(register_form.cleaned_data['password_1'])
            user.is_active = False
            user.save()
            
            # Setup email
            current_site = get_current_site(request)
            subject = 'Activate your Account'
            message = render_to_string('account/registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject=subject, message=message)
            return render(request, 'account/registration/email_activation.html')
        else:
            return render(request, 'account/registration/register.html', {'form': register_form})
    else:
        register_form = RegistrationForm()
        return render(request, 'account/registration/register.html', {'form': register_form})


def account_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserBase.objects.get(pk=uid)
    except ValueError as e:
        print(e)
        return render(request, 'account/registration/activation_invalid.html')
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('account:dashboard')
    else:
        return render(request, 'account/registration/activation_invalid.html')


@login_required
def dashboard(request):
    return render(request, 'account/user/dashboard.html', context={})


# class UserLoginView(LoginView):
#     template_name = 'account/registration/login.html',
#     form_class = UserLoginForm,


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('store:product_all')


def edit_details(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        
        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
    
    return render(request, 'account/user/edit_details.html', {'form': user_form})


@login_required
def delete_user(request):
    user = UserBase.objects.get(email=request.user.email)
    logout(request)
    user.is_active = False
    user.save()
    return render(request, 'account/user/delete.html')


class UserPasswordResetView(PasswordResetView):
    email_template_name = 'account/user/password_reset_email.html'
    form_class = UserPasswordResetForm
    template_name = 'account/user/reset_password.html'
    success_url = reverse_lazy('account:reset_password_sent')


class UserPasswordResetConfirm(PasswordResetConfirmView):
    form_class = SetUserPasswordForm
    success_url = reverse_lazy('account:password_reset_complete')
    template_name = 'account/user/reset_password_confirm.html'
    
    
class UserPasswordChangeView(PasswordChangeView):
    template_name = 'account/user/change_password.html'
    success_url = reverse_lazy('account:dashboard')
    form_class = UserPasswordChangeForm
    
