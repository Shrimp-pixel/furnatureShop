import hashlib
from django.conf import settings

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django import forms

from .models import ShopUser, ShopUserProfile
import pytz
from datetime import datetime, timedelta


class ValidAge:

    def clean_age(self):
        data = self.cleaned_data['age']
        if data < 18:
            raise forms.ValidationError('Слишком молод!')
        elif data > 100:
            raise forms.ValidationError('Слишком стар!')
        return data


class ShopUserLoginForm(AuthenticationForm):
    class Meta:
        model = ShopUser
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class ShopUserRegisterForm(UserCreationForm, ValidAge):
    class Meta:
        model = ShopUser
        fields = ['username', 'avatar', 'email', 'age', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if hasattr(field.widget, 'input_type') and field.widget.input_type == 'checkbox':
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

    def save(self, *args, **kwargs):
        user = super().save(*args, **kwargs)
        user.is_active = False
        user.activate_key = hashlib.sha1(user.email.encode('utf8')).hexdigest()

        user.activate_key_expired = datetime.now(pytz.timezone(settings.TIME_ZONE))
        user.save()

        print(user.activate_key)

        return user


class ShopUserEditForm(UserChangeForm, ValidAge):
    class Meta:
        model = ShopUser
        fields = ['username', 'first_name', 'last_name', 'avatar', 'email', 'age', 'password', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():

            if hasattr(field.widget, 'input_type') and field.widget.input_type == 'checkbox':
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
            if field_name == 'password':
                field.widget = forms.HiddenInput()
                field.help_text = ''


class ShopUserProfileEditForm(forms.ModelForm):
    class Meta:
        model = ShopUserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if hasattr(field.widget, 'input_type') and field.widget.input_type == 'checkbox':
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
