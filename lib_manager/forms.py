from django import forms
from django.core.validators import RegexValidator

from .models import Reader

class LogIn(forms.Form):
    """Форма выбора пользователя"""
    readers = forms.ModelChoiceField(queryset=Reader.objects.all(), label="Войти как", )


class Register(forms.ModelForm):
    class Meta:
        model = Reader
        fields = ["last_name", "first_name", "middle_name"]

class BookCode(forms.Form):
    code = forms.CharField(
        label="Код",
        max_length=4,
        validators=[
            RegexValidator(
                regex=r'^\d{4}$',  # Проверка на четыре цифры
                message='Код должен содержать ровно четыре цифры',
                code='invalid_code'
            )
        ]
    )
    def clean_code(self):
        code = self.cleaned_data.get('code')
        if code:
            try:
                return int(code)
            except ValueError:
                raise forms.ValidationError('Код должен быть целым числом.')