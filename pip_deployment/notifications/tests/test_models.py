from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase

from notifications.models import Notification


class NotificationModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a user for testing
        User = get_user_model()
        cls.user = User.objects.create_user(username='testuser', password='testpass')

    def test_notification_creation(self):
        # Create a notification
        notification = Notification.objects.create(
            user=self.user,
            content='Test content',
            type='Test type'
        )

        # Verify the notification was created correctly
        self.assertEqual(notification.user, self.user)
        self.assertEqual(notification.is_read, False)
        self.assertEqual(notification.content, 'Test content')
        self.assertEqual(notification.type, 'Test type')
        self.assertIsInstance(notification.created_at, datetime)
