from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.models import User
from django.db.models import QuerySet

from .models import Notification
from .serializers import NotificationSerializer


def send_message(message, user, type: str):
    channel_layer = get_channel_layer()
    if isinstance(user, User):
        # Single user
        users = [user]
    elif isinstance(user, QuerySet):
        # QuerySet of users
        users = user
    else:
        raise ValueError("Invalid user argument. Expected User or QuerySet.")

    for recipient in users:
        notification = Notification.objects.create(user=recipient, content=message, type=type)

        async_to_sync(channel_layer.group_send)(
            get_user_inbox_key(notification.user.id),
            {
                'type': 'notification',
                'notification_type': type,
                'data': dict(NotificationSerializer(notification).data)
            }
        )


def get_user_inbox_key(user_id):
    return f'inbox_{user_id}'
