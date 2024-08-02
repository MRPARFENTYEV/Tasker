from django import forms
from .models import User

class UserLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'email'}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'password'}
        )
    )


class UserRegistrationForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'email'}
        )
    )
    full_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'full name'}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'password'}
        )
    )

class AddTaskForm(forms.Form):

    title = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Тема'})
    )
    description = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Описание'})
    )

class DelTaskForm(forms.Form):

    task_id = forms.IntegerField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Введите номер задачи, которую хотите удалить'})
    )
class DelegateTaskForm(forms.Form):

    task_id = forms.IntegerField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Введите номер задачи, которую хотите делегировать'})
    )
    realizer_id = forms.IntegerField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Введите номер сотрудника, кому хотите делегировать'})
    )



