from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from rest_framework import status
from rest_framework.test import APIRequestFactory

from ..models import Notification
from ..serializers import NotificationSerializer
from ..views import FetchUnreadNotifications, FetchAllNotifications, MarkAllNotificationsAsRead


class NotificationViewTestCase(TestCase):
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

    def test_fetch_unread_notifications(self):
        factory = APIRequestFactory()
        view = FetchUnreadNotifications.as_view()

        request = factory.get('/unread/')
        request.user = self.user

        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        notifications = Notification.objects.filter(user=self.user, is_read=False)
        serializer = NotificationSerializer(notifications, many=True)

        self.assertEqual(response.data, serializer.data)

    def test_fetch_all_notifications(self):
        factory = APIRequestFactory()
        view = FetchAllNotifications.as_view()

        request = factory.get('/all/')
        request.user = self.user

        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        notifications = Notification.objects.all()
        serializer = NotificationSerializer(notifications, many=True)

        self.assertEqual(response.data, serializer.data)

    def test_mark_all_notifications_as_read(self):
        factory = APIRequestFactory()
        view = MarkAllNotificationsAsRead.as_view()

        request = factory.put('/mark/')
        request.user = self.user

        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify that all notifications are marked as read
        notifications = Notification.objects.filter(user=self.user)
        for notification in notifications:
            self.assertTrue(notification.is_read)
