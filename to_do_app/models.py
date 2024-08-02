from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, email, full_name, password, ):
        if not email:
            raise ValueError('Email is required!')
        if not full_name:
            raise ValueError('full name is required!')

        user = self.model(email=self.normalize_email(email), full_name=full_name)
        user.set_password(password)
        user.save(using=self.db)
        return user
class User(AbstractBaseUser):
    email = models.EmailField(max_length=100, unique=True)
    full_name = models.CharField(max_length=100)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']
    search_fields =['full_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email


class Tasks(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    is_done = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='user_tasks', on_delete=models.CASCADE)






