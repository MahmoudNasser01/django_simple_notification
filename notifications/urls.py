from django.urls import path

from .views import FetchAllNotifications, FetchUnreadNotifications, MarkAllNotificationsAsRead

app_name = 'notifications'

urlpatterns = [
    path('all/', FetchAllNotifications.as_view(), name='list'),
    path('unread/', FetchUnreadNotifications.as_view(), name='unread'),
    path('mark/', MarkAllNotificationsAsRead.as_view(), name='mark'),
]
