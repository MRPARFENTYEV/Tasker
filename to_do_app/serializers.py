from rest_framework import serializers

from to_do_app.models import Tasks, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'full_name']


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = ['id', 'title', 'description', 'is_done', 'created']
