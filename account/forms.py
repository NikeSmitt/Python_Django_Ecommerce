from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm, UserChangeForm, \
    PasswordChangeForm
from django.contrib.auth.password_validation import validate_password

from .models import UserBase


class RegistrationForm(forms.ModelForm):
    user_name = forms.CharField(label='Enter Username', help_text='Required')
    email = forms.EmailField(help_text='Required', error_messages={'required': 'You need an email'})
    password_1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password_2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.fields['user_name'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Username'}
        )
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Email'}
        )
        self.fields['password_1'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Password'}
        )
        self.fields['password_2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Repeat password'}
        )
    
    def clean_user_name(self):
        user_name = self.cleaned_data['user_name'].lower()
        if UserBase.objects.filter(user_name=user_name).exists():
            raise forms.ValidationError('Username already exists')
        return user_name
    
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if UserBase.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exists')
        return email
    
    def clean_password_1(self):
        password = self.cleaned_data['password_1']
        validate_password(password)
        return password
    
    def clean_password_2(self):
        cd = self.cleaned_data
        if cd.get('password_1') and cd['password_1'] != cd['password_2']:
            raise forms.ValidationError('Passwords do not match')
        return cd['password_2']
    
    class Meta:
        model = UserBase
        fields = ('user_name', 'email',)


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Username', 'id': 'login-username'}
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'id': 'login-pwd',
        }
    ))


class UserEditForm(UserChangeForm):
    email = forms.EmailField(label='Account email (can not be changed)', widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'email', 'id': 'form-email', 'readonly': 'readonly'}
    ))
    user_name = forms.CharField(label='Username', widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'username', 'id': 'form-username'}
    ))
    first_name = forms.CharField(label='First name', widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'First Name', 'id': 'form-first-name'}
    ))
    
    class Meta:
        model = UserBase
        fields = ('email', 'user_name', 'first_name',)
    
    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['user_name'].required = True


class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(max_length=255,
                             label='Enter you email',
                             widget=forms.TextInput(
                                 attrs={'class': 'form-control mb-3', 'placeholder': 'email', 'id': 'form-email', }
                             ))
    
    def clean_email(self):
        email = self.cleaned_data['email']
        u = UserBase.objects.filter(email=email)
        if not u:
            raise forms.ValidationError(
                'Unfortunately we can not find that email address')
        return email


class SetUserPasswordForm(SetPasswordForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['new_password1'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'New password'}
        )

        self.fields['new_password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'New password'}
        )


class UserPasswordChangeForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super(UserPasswordChangeForm, self).__init__(*args, **kwargs)
        
        self.fields['old_password'].widget.attrs.update({
            'class': 'form-control mb-3', 'placeholder': 'Old password',
        })
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control mb-3', 'placeholder': 'Old password',
        })
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Old password',
        })
        