from django.utils.translation import gettext_lazy as _
from django import forms
from django.contrib.auth.forms import UsernameField
from django.contrib.auth import (
     password_validation
)
from django.contrib.auth import models

class RegisterForm(forms.ModelForm):
    username = UsernameField(
        max_length=16,
        error_messages={
            'max_length': '名稱超過長度限制',
            'unique': _("名稱已被人使用"),
            'invalid': '請輸入有效名稱',
            'required': '尚未輸入使用者名稱'
        }
    )
    password1 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
        error_messages={
             'required': '尚未輸入密碼',
         }
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        error_messages={'required': '尚未輸入確認密碼'}
    )
    error_messages = {
        'password_mismatch': _('兩次密碼輸入不同'),
    }
    class Meta:
        model = models.User
        fields = ("username","password1","password2")
        #field_classes = {'username': UsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs['autofocus'] = True            
            
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password2', error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
