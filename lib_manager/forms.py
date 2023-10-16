from django import forms

from .models import Reader

class LogIn(forms.Form):
    """Форма выбора пользователя"""
    readers = forms.ModelChoiceField(queryset=Reader.objects.all(), label="Войти как", )


class Register(forms.ModelForm):
    class Meta:
        model = Reader
        fields = ["last_name", "first_name", "middle_name"]