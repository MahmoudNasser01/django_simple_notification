from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from notifications.models import Notification


class NotificationURLTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a user for testing
        User = get_user_model()
        cls.user = User.objects.create_user(username='testuser', password='testpass')

    def setUp(self):
        # Create some sample notifications
        Notification.objects.create(
            user=self.user,
            content='Notification 1',
            is_read=False,
            type='Type 1'
        )
        Notification.objects.create(
            user=self.user,
            content='Notification 2',
            is_read=True,
            type='Type 2'
        )
        # Create a client for making requests
        self.client = Client()
        # Log in the user
        self.client.login(username='testuser', password='testpass')

    def test_fetch_all_notifications(self):
        url = reverse('notification:list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Notification 1')
        self.assertContains(response, 'Notification 2')

    def test_fetch_unread_notifications(self):
        url = reverse('notification:unread')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Notification 1')
        self.assertNotContains(response, 'Notification 2')

    def test_mark_all_notifications_as_read(self):
        url = reverse('notification:mark')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)

        # Verify that all notifications are marked as read
        notifications = Notification.objects.filter(user=self.user)
        for notification in notifications:
            self.assertTrue(notification.is_read)
