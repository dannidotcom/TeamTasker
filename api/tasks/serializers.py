from rest_framework import serializers
from .models import Project, Task, Notification
from django.contrib.auth.models import User

# Serializer pour l'utilisateur
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

# Serializer pour le modèle Project
class ProjectSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    task_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'created_at', 'updated_at', 'owner', 'task_count']

# Serializer pour le modèle Task
    
class TaskSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)
    assigned_to = UserSerializer(read_only=True)
    is_overdue = serializers.BooleanField(read_only=True)  

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'status', 'priority', 'start_date', 'due_date',
            'assigned_to', 'project', 'created_at', 'updated_at', 'is_overdue'
        ]

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['created_by'] = request.user
        task = Task.objects.create(**validated_data)
        return task

    def update(self, instance, validated_data):
        request = self.context.get('request')
        validated_data['updated_by'] = request.user
        return super().update(instance, validated_data)
    
# Serializer pour le modèle Notification
class NotificationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'message', 'user', 'read', 'created_at', 'updated_at']

    def mark_as_read(self, instance):
        instance.read = True
        instance.save()
        return instance
