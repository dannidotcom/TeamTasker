
from ..models import Notification

class NotificationService:
    """Service pour la gestion des notifications."""

    def send_notification(self, user, message):
        """Crée et envoie une notification à l'utilisateur spécifié."""
        notification = Notification.objects.create(
            user=user,
            message=message,
            created_by=user  # Optionnel : peut être ajusté en fonction du contexte
        )
        return notification

    def mark_as_read(self, notification):
        """Marque la notification comme lue."""
        notification.read = True
        notification.save()
        return notification
