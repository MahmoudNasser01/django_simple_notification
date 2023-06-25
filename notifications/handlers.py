from abc import ABC, abstractmethod

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from django.db.models.query import QuerySet

from .models import Notification
from .serializers import NotificationSerializer

User = get_user_model()

channel_layer = get_channel_layer()


class AbstractSendMessage(ABC):
    def _save_notifications(self) -> list[Notification]:
        """A method for creating new notification records

        Returns:
            list: a list of new notifications objects
        """

        notifications_list = [
            Notification(user=user, content=self.message, type=self.type) for user in self.users
        ]
        notifications = Notification.objects.bulk_create(notifications_list)
        return notifications

    def __init__(self, users: QuerySet, message: str, no_type: str) -> None:
        """
        Args:
            users (QuerySet): a queryset from user model
            message (str): the notification that will be send to the users
            no_type (str): the notifications type
        """

        if isinstance(users, User):
            self.users = [users]
        elif isinstance(users, QuerySet) and type(users.first()) is User:
            self.users = users
        else:
            raise ValueError(
                f'Cannot assign "{type(users)}": "Notification.user" must be a "User" instance.'
            )

        self.message = message
        self.type = no_type
        self.notifications = self._save_notifications()

    @abstractmethod
    def send_message(self):
        """
        abstractmethod for sending notifications through django channels
        """
        pass


class SendMessage(AbstractSendMessage):
    def send_message(self) -> None:

        for notification in self.notifications:
            async_to_sync(channel_layer.group_send)(
                get_user_inbox_key(notification.user.id),
                {
                    "type": "notification",
                    "notification_type": self.type,
                    "data": dict(NotificationSerializer(notification).data),
                },
            )


def get_user_inbox_key(user_id):
    return f"inbox_{user_id}"
