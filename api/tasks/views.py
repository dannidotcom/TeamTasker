
from .service.task_service import TaskService
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Project, Task, Notification
from .serializers import ProjectSerializer, TaskSerializer, NotificationSerializer

from .service.notification_service import NotificationService

# Vue pour la liste et la création de projets
class ProjectListCreateView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user, created_by=self.request.user)

# Vue pour le détail et la mise à jour de projet
class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

# Vue pour la liste et la création de tâches
class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        request = self.request
        task_service = TaskService()
        task = task_service.create_task(
            title=serializer.validated_data['title'],
            description=serializer.validated_data.get('description'),
            project=serializer.validated_data['project'],
            assigned_to=serializer.validated_data.get('assigned_to'),
            created_by=request.user
        )
        notification_service = EmailNotificationService()
        if task.assigned_to:
            notification_service.send_notification(
                task.assigned_to, f"Nouvelle tâche assignée : {task.title}"
            )

# Vue pour le détail, la mise à jour et la suppression de tâches
class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

# Vue pour la liste et la création de notifications
class NotificationListView(generics.ListCreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

# Vue pour marquer une notification comme lue
class MarkNotificationAsReadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            notification = Notification.objects.get(pk=pk, user=request.user)
            serializer = NotificationSerializer().mark_as_read(notification)
            return Response(
                {"message": "Notification marquée comme lue."},
                status=status.HTTP_200_OK
            )
        except Notification.DoesNotExist:
            return Response(
                {"error": "Notification introuvable ou non autorisée."},
                status=status.HTTP_404_NOT_FOUND
            )
        
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
@api_view(['POST'])
def register_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email', '')

    if not username or not password:
        return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password, email=email)
    token, created = Token.objects.get_or_create(user=user)

    return Response({'token': token.key}, status=status.HTTP_201_CREATED)