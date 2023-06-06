from enum import Enum

from django.contrib.auth.models import User
from django.db import models

from notifications.handlers import send_message


class NotificationsTypes(Enum):
    NEW_ORDER = 'NEW_ORDER'
    ORDER_CANCELLED = 'ORDER_CANCELLED'


class Order(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


# create a signal on create new order
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Order)
def create_order(sender, instance, created, **kwargs):
    if created:
        # send notification
        send_message(f'New order created with name: {instance.name} and address {instance.address}', instance.owner, NotificationsTypes.NEW_ORDER.value)
