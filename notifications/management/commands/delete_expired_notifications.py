from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings

from notifications.models import Notification


class Command(BaseCommand):
    help = "custom django command to delete expired notifications after exceeding a certain time period, defined in days"
    
    def handle(self, *args, **options):

        # default to 30 days if value is not configured in settings        
        notifications_life_period = getattr(settings,"NOTIFICATIONS_LIFE_PERIOD", 30)
        
        print(
            f"\n start deleting notifications older than {notifications_life_period} days ...\n"
        )

        expired_notifications = Notification.objects.exclude(
            created_at__gt=timezone.now() - timedelta(days=notifications_life_period)
        )

        n_expired_notifications = expired_notifications.count()
        expired_notifications.delete()

        print(
           f"\n--- {n_expired_notifications} expired notifications are deleted from the database ---\n"
        )
