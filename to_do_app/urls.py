from to_do_app import views
from django.urls import path
from rest_framework.routers import DefaultRouter

app_name = 'to_do_app'

rout = DefaultRouter()
rout.register('tasks', views.TaskViewSet)
rout.register('users', views.UserViewSet)
urlpatterns = [
    path('register/', views.user_register, name='user_register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    # path('main_page/', views.main_page, name='main_page'),
    path('all_tasks/', views.return_tasks, name='return_tasks'),
    path('', views.home_page, name='home_page')

]
# + rout.urls