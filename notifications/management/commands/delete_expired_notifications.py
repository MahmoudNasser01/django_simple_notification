from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from notifications.models import Notification


class Command(BaseCommand):
    help = "custom django command to delete expired notifications after exceeding a specified time period"
    
    def add_arguments(self, parser):
        parser.add_argument(
            "--period",
            type=int,
            default=30,
            help="time period in days"
        )

    def handle(self, *args, **options):
        n_days_provided = options["period"]
        
        print(
            f"\n start deleting notifications older than {n_days_provided} days ...\n"
        )

        expired_notifications = Notification.objects.exclude(
            created_at__gt=timezone.now() - timedelta(days=n_days_provided)
        )

        n_expired_notifications = expired_notifications.count()
        expired_notifications.delete()

        print(
            f"\n--- {n_expired_notifications} expired notifications are deleted from the database ---\n"
        )
