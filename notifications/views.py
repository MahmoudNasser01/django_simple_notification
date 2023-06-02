from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from notifications.models import Notification
from notifications.serializers import NotificationSerializer


def index(request):
    return render(request, 'notifications_index.html')


class FetchUnreadNotifications(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        notifications = Notification.objects.filter(user=request.user, is_read=False)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FetchAllNotifications(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        notifications = Notification.objects.all()
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MarkAllNotificationsAsRead(APIView):
    def put(self, request):
        Notification.objects.filter(user=request.user).update(is_read=True)
        return Response(status=status.HTTP_200_OK)
