import datetime
from django.http import HttpResponse, JsonResponse

from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.core.paginator import Paginator
from .models import User,Tasks
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.viewsets import ViewSet, ModelViewSet
# from .permissions import IsOwnerOrReadOnly
from to_do_app.serializers import TaskSerializer,UserSerializer

'''Тут можно crud`ить сколько угодно, только в url раскоментировать # + rout.urls'''
# ___________________________________
class TaskViewSet(ModelViewSet):
    queryset = Tasks.objects.all()
    serializer_class = TaskSerializer

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class=UserSerializer


'''А вот тут я делаю как считаю нужным, без фронтенда не обойтись'''
# https://docs.djangoproject.com/en/5.0/topics/pagination/
def paginat(request, list_objects:list):

    p = Paginator(list_objects, 2)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    return page_obj

def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(
                data['email'], data['full_name'], data['password'],
            )
            context = {'notice': 'Перейдите по ссылке'}
            return redirect('to_do_app:main_page')

    else:
        form = UserRegistrationForm()
    context = {'title':'Signup', 'form':form}
    return render(request, 'register.html', context)

def return_tasks(request):
    user = request.user
    tasks = Tasks.objects.filter(user=user)
    context ={'tasks':tasks}
    return render(request, 'all_tasks.html', context)

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request, email=data['email'], password=data['password']
            )
            if user is not None:
                login(request, user)

                return redirect('to_do_app:home_page')
            else:
                messages.error(
                    request, 'Имя или пароль неверны', 'danger'
                )
                return redirect('to_do_app:user_login')
    else:
        form = UserLoginForm()
    context = {'title': 'Login', 'form': form}
    return render(request, 'login.html', context)

def user_logout(request):
    logout(request)
    return redirect('to_do_app:user_login')
# def main_page(request):
#     context = {}
#     return render(request, 'all_tasks.html', context)

def home_page(request):
    user = request.user
    context = {}
    print(request.user)
    if str(request.user) == 'AnonymousUser':
        return redirect('to_do_app:user_login')
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        title = request.POST.get('title')
        description = request.POST.get('description')
        is_done = request.POST.get('is_done') == 'true'

        task = Tasks.objects.get(id=task_id, user_id=user.id)
        task.title = title
        task.description = description
        task.is_done = is_done
        user = user.id
        task.save()
        return JsonResponse({'success': True})
    else:
        user = request.user
        tasks = Tasks.objects.filter(user_id=user)
        for task in tasks:
            context['Тема:'] = task.title
            context['Описание:'] = task.description
            if task.is_done == False:
                context['Выполнено:'] = 'Не выполнено'
            else:context['Выполнено:'] = 'Выполнено'
        print(context)

        return render(request, 'home.html', context={'tasks': paginat(request, tasks)})
def add_task(request):
    user = request.user
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form = UserRegistrationForm(request.POST) # изменить форму
            data = form.cleaned_data
            print(data)
            # task = Tasks.objects.create(title=data['title'],
            #                             description=data['description'],
            #                             created_at=datetime.datetime.now(),user_id=user.id)


#
# # Create your views here.
# def user_login(request):
#     if request.method == 'POST':
#         form = UserLoginForm(request.POST)
#
#         if form.is_valid():
#             data = form.cleaned_data
#             print(data)
#             user = authenticate(
#
#                 request, email=data['email'], password=data['password']
#             )
#             print(user)
#             if user is not None:
#
#                 login(request, user)
#                 return redirect('shop:home_page')
#             else:
#                 messages.error(
#                     request, 'Имя или пароль не верны', 'danger'
#                 )
#                 return redirect('accounts:user_login')
#     else:
#         form = UserLoginForm()
#     context = {'title':'Login', 'form': form}
#     return render(request, 'login.html', context)