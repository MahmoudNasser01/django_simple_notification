from django.contrib import admin

from .models import Notification


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_read', 'content', 'type', 'created_at')
    list_filter = ('user', 'is_read', 'type', 'created_at')


admin.site.register(Notification, NotificationAdmin)
