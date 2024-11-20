from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Modèle de base pour inclure les champs communs
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='%(class)s_created')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='%(class)s_updated')

    class Meta:
        abstract = True

    def mark_updated(self, user):
        """Marque l'objet comme mis à jour par un utilisateur spécifique."""
        self.updated_by = user
        self.save()

# Modèle Projet
class Project(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_projects')

    def __str__(self):
        return self.name

    @property
    def task_count(self):
        """Retourne le nombre total de tâches associées à ce projet."""
        return self.tasks.count()

# Modèle Tâche
class Task(BaseModel):
    STATUS_CHOICES = [
        ('TO_DO', 'À faire'),
        ('IN_PROGRESS', 'En cours'),
        ('DONE', 'Terminé')
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='TO_DO')
    priority = models.IntegerField(default=1)
    start_date = models.DateField()
    due_date = models.DateField()
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_tasks')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        return self.title

    def is_overdue(self):
        """Vérifie si la tâche est en retard."""
        return self.due_date < date.today() and self.status != 'DONE'

    def assign_to(self, user):
        """Attribue la tâche à un utilisateur et marque la mise à jour."""
        self.assigned_to = user
        self.mark_updated(user)

# Modèle Notification
class Notification(BaseModel):
    message = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    read = models.BooleanField(default=False)

    def __str__(self):
        return f'Notification for {self.user.username}: {self.message}'

    def mark_as_read(self):
        """Marque la notification comme lue."""
        self.read = True
        self.save()
