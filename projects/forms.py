from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm

TAILWIND_INPUT = 'w-full bg-slate-950 border border-slate-800 rounded px-3 py-2 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-sky-500 transition'

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': TAILWIND_INPUT})
            field.help_text = None

        if 'username' in self.fields:
            self.fields['username'].widget.attrs.update({'placeholder': 'Choose a username (e.g. alex)'})
        if 'password1' in self.fields:
            self.fields['password1'].widget.attrs.update({'placeholder': 'Create password (min 8 chars)'})
        if 'password2' in self.fields:
            self.fields['password2'].widget.attrs.update({'placeholder': 'Re-enter your password'})


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': TAILWIND_INPUT})

        self.fields['first_name'].widget.attrs.update({'placeholder': 'Your first name'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Your last name'})
        self.fields['email'].widget.attrs.update({'placeholder': 'you@example.com'})
        self.fields['email'].widget.input_type = 'email'


class StyledPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': TAILWIND_INPUT})
            field.help_text = None

        self.fields['old_password'].widget.attrs.update({'placeholder': 'Current password'})
        self.fields['new_password1'].widget.attrs.update({'placeholder': 'New password (min 8 chars)'})
        self.fields['new_password2'].widget.attrs.update({'placeholder': 'Confirm new password'})
