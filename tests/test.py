from to_do_app import models
from to_do_app import views
import pytest
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpRequest
from your_app.views import paginat

@pytest.mark.django_db
def test_paginat_first_page():
    request = HttpRequest()
    request.GET['page'] = '1'
    list_objects = ['obj1', 'obj2', 'obj3', 'obj4']
    page_obj = paginat(request, list_objects)
    assert list(page_obj) == ['obj1', 'obj2']

@pytest.mark.django_db
def test_paginat_second_page():
    request = HttpRequest()
    request.GET['page'] = '2'
    list_objects = ['obj1', 'obj2', 'obj3', 'obj4']
    page_obj = paginat(request, list_objects)
    assert list(page_obj) == ['obj3', 'obj4']

@pytest.mark.django_db
def test_paginat_invalid_page():
    request = HttpRequest()
    request.GET['page'] = 'invalid'
    list_objects = ['obj1', 'obj2', 'obj3', 'obj4']
    page_obj = paginat(request, list_objects)
    assert list(page_obj) == ['obj1', 'obj2']

@pytest.mark.django_db
def test_paginat_empty_page():
    request = HttpRequest()
    request.GET['page'] = '10'
    list_objects = ['obj1', 'obj2', 'obj3', 'obj4']
    page_obj = paginat(request, list_objects)
    assert list(page_obj) == ['obj3', 'obj4']

