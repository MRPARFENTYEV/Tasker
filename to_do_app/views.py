from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework.viewsets import ModelViewSet
from to_do_app.serializers import TaskSerializer, UserSerializer
from .forms import UserRegistrationForm, UserLoginForm, AddTaskForm, DelTaskForm, DelegateTaskForm
from .models import User, Tasks, Delegation

'''Тут можно crud`ить сколько угодно, только в url раскоментировать # + rout.urls'''
# ___________________________________
class TaskViewSet(ModelViewSet):
    queryset = Tasks.objects.all()
    serializer_class = TaskSerializer

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class=UserSerializer



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
            return redirect('to_do_app:home_page')

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


def home_page(request):
    user = request.user
    context = {}
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


        return render(request, 'home.html', context={'tasks': paginat(request, tasks)})
def add_task(request):
    user = request.user
    if request.method == 'POST':
        form = AddTaskForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            task = Tasks.objects.create(title=data['title'],
                                        description=data['description'],user_id=user.id)

            return redirect('to_do_app:home_page')
    else:
        form = AddTaskForm()
    context = {'form': form}
    return render(request, 'add_task.html', context)


def del_task(request):
    user = request.user
    tasks = Tasks.objects.filter(user_id=user.id)

    if request.method == 'POST':
        form = DelTaskForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                # Удаление задачи по переданному идентификатору
                task = Tasks.objects.get(id=data['task_id'], user=user)
                task.delete()
                return redirect('to_do_app:home_page')
            except Tasks.DoesNotExist:
                form.add_error(None, 'Задача не найдена или у вас нет прав на её удаление.')

    else:
        form = DelTaskForm()

    context = {'form': form, 'tasks': tasks}
    return render(request, 'del_task.html', context)

def delegate_task(request):
    context = {}
    users = User.objects.exclude(id=request.user.id)
    tasks = Tasks.objects.filter(user_id=request.user.id)
    context['users'] = users
    context['tasks'] = tasks

    if request.method == 'POST':
        form = DelegateTaskForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                task = Tasks.objects.get(id=data['task_id'], user=request.user)
                realizer = User.objects.get(id=data['realizer_id'])
                Delegation.objects.create(owner=request.user, task_id=task, realizer=realizer)
                return redirect('to_do_app:home_page')
            except (Tasks.DoesNotExist, User.DoesNotExist):
                form.add_error(None, 'Задача или пользователь не найдены.')
    else:
        form = DelegateTaskForm()

    context['form'] = form
    return render(request, 'delegation.html', context)


def show_delegated(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        is_done = request.POST.get('is_done') == 'true'

        try:
            task = Tasks.objects.get(id=task_id)
            task.is_done = is_done
            task.save()
            return JsonResponse({'success': True})
        except Tasks.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Не найдено'})

    delegations = Delegation.objects.filter(realizer=request.user).select_related('task_id', 'owner')
    context = {
        'delegations': delegations
    }
    return render(request, 'show_delegated.html', context)



