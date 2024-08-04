from to_do_app import views
from django.urls import path
from rest_framework.routers import DefaultRouter

app_name = 'to_do_app'

# rout = DefaultRouter()
# rout.register('tasks', views.TaskViewSet)
# rout.register('users', views.UserViewSet)
urlpatterns = [
    path('register/', views.user_register, name='user_register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('all_tasks/', views.return_tasks, name='return_tasks'),
    path('', views.home_page, name='home_page'),
    path('add_task/',views.add_task, name='add_task'),
    path('del_task/',views.del_task, name='del_task'),
    path('delegate_task/',views.delegate_task, name='delegate_task'),
    path('show_delegated/',views.show_delegated, name='show_delegated')



]
# + rout.urls