from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'w-full bg-slate-950 border border-slate-800 rounded px-3 py-2 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-sky-500 transition',
            })
            # Remove verbose default help texts that break dark mode styling
            field.help_text = None

        if 'username' in self.fields:
            self.fields['username'].widget.attrs.update({'placeholder': 'Choose a username (e.g. alex)'})
        if 'password1' in self.fields:
            self.fields['password1'].widget.attrs.update({'placeholder': 'Create password (min 8 chars)'})
        if 'password2' in self.fields:
            self.fields['password2'].widget.attrs.update({'placeholder': 'Re-enter your password'})
