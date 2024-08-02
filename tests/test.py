from to_do_app.models import User, Tasks, Delegation
from to_do_app import views
import pytest
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpRequest
from django.test import Client
from django.urls import reverse

@pytest.mark.django_db
def test_user_register_post_valid():
    client = Client()
    form_data = {
        'email': 'test@example.com',
        'full_name': 'Test User',
        'password': 'password123',
    }
    response = client.post(reverse('to_do_app:user_register'), data=form_data)
    assert response.status_code == 302  # Redirects after successful registration
    assert User.objects.filter(email='test@example.com').exists()

@pytest.mark.django_db
def test_user_register_post_valid():
    client = Client()
    response = client.get('login/')
    assert response.status_code == 200  # Redirects after successful registration
