
from ..models import Task

class TaskService:
    """Service pour la gestion des tâches."""

    def create_task(self, title, description, project, assigned_to, created_by):
        """Crée une nouvelle tâche et retourne l'instance."""
        task = Task.objects.create(
            title=title,
            description=description,
            project=project,
            assigned_to=assigned_to,
            created_by=created_by
        )
        return task

    def update_task_status(self, task, status, updated_by):
        """Met à jour le statut de la tâche."""
        task.status = status
        task.updated_by = updated_by
        task.save()
        return task
