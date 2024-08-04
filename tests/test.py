from to_do_app.models import User, Tasks, Delegation
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.test import Client

@pytest.mark.django_db
def test_user_login(client):
    # Создание пользователя для тестирования
    user = get_user_model().objects.create_user(
        full_name='testuser',
        email='test@example.com',
        password='password123'
    )

    # URL логина
    url = reverse('to_do_app:user_login')

    # Отправка POST запроса с правильными данными
    response = client.post(url, {'email': 'test@example.com', 'password': 'password123'})
    assert response.status_code == 302  # Перенаправление на главную страницу# passed
    assert response.url == reverse('to_do_app:home_page')  # Проверка URL перенаправления # passed

    # # Отправка POST запроса с неправильными данными
    response = client.post(url, {'email': 'test@example.com', 'password': 'wrongpassword'})
    # assert response.status_code == 302  # Перенаправление обратно на страницу логина # passed
    # assert response.url == reverse('to_do_app:user_login')  # Проверка URL перенаправления # passed

@pytest.fixture
def client():
    return Client()

def test_user_logout(client):
    response = client.get(reverse('to_do_app:user_login'))
    assert response.status_code == 200  # код перенаправления


# @pytest.fixture
# def task():
#     task = Tasks(title='Пример задачи', description='Это пример описания задачи')
#     task.save()
#     return task


# def test_home_page(client, task):
#     response = client.get(reverse('home_page'))
#     assert response.status_code == 200  # код страницы
#     context = response.context
#     assert context['Тема:'] == task.title  # проверка заголовка
#     assert context['Описание:'] == task.description  # проверка описания
#     assert not context['Выполнено:']  # проверка статуса выполнения
#     assert 'tasks' in response.context  # проверка наличия словаря задач
