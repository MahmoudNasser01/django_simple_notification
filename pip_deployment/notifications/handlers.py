from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .models import Notification
from .serializers import NotificationSerializer

channel_layer = get_channel_layer()


def send_message(message, user, type: str):
    notification = Notification.objects.create(user=user, content=message, type=type)

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
