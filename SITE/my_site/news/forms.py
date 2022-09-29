from django import forms
from django.contrib.auth import password_validation

from .models import Category, News
import re
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


# class NewsForm(forms.Form):     Форма, не связанная с моделью
#    title = forms.CharField(max_length=150, label='Название', widget=forms.TextInput(attrs={'class': 'form-control'}))
#    content = forms.CharField(label='Текст', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
#    is_published = forms.BooleanField(label='Опубликовано', initial=True)
#    category = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), label='Категория',
#                                      empty_label='Выберите категорию', queryset=Category.objects.all())


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Введите имя пользователя',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Введите пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(
        label=_('Имя пользователя'),
        help_text=_('Обязательное поле. Не более 150 символов. Только буквы, цифры и символы @/./+/-/_.'),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label=_('Адрес электронной почты'),
        widget=forms.EmailInput(attrs={"autocomplete": "email", 'class': 'form-control'})
    )
    password1 = forms.CharField(
        label=_('Введите пароль'),
        widget=forms.PasswordInput(attrs={'class': 'form-control', "autocomplete": "new-password", 'placeholder': '12345'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_('Повторите введенный пароль'),
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text=_("Повторно введите пароль. Регистр букв важен!")
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class NewsForm(forms.ModelForm):  # Форма, связанная с моделью
    class Meta:  # Описание, как должна выглядеть форма
        model = News  # С какой моделью будет связана форма
        # fields = '__all__' # Если нужны все поля из формы
        fields = ['title', 'content', 'is_published', 'category', 'photo']  # Указываем, какие поля нужны из формы
        widgets = {'title': forms.TextInput(attrs={'class': 'form-control'}),
                   'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
                   'category': forms.Select(attrs={'class': 'form-select'})
                   }

    def clean_title(self):  # Создал кастомный валидатор
        title = self.cleaned_data['title']
        if re.match(r'\d', title):
            raise ValidationError('Название не должно начинаться с цифры')
        return title
