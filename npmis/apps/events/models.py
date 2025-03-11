from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

from actstream.models import Action

from .managers import EventSubscriptionManager, NotificationManager, ObjectEventSubscriptionManager
from .mixins import NotificationBusinessLogicMixin, StoredEventTypeBusinessLogicMixin


class StoredEventType(StoredEventTypeBusinessLogicMixin, models.Model):
    """
    Model to mirror the real event classes as database objects.
    """
    name = models.CharField(
        max_length=64, unique=True, verbose_name=_(message='Name')
    )

    class Meta:
        db_table = 'storedeventtype'

        verbose_name = _(message='Stored event type')
        verbose_name_plural = _(message='Stored event types')

    def __str__(self):
        return str(self.label)


class EventSubscription(models.Model):
    """
    This model stores the event subscriptions of a user for the entire
    system.
    """
    user = models.ForeignKey(
        db_index=True, on_delete=models.CASCADE,
        related_name='event_subscriptions', to=settings.AUTH_USER_MODEL,
        verbose_name='User'
    )
    stored_event_type = models.ForeignKey(
        on_delete=models.CASCADE, related_name='event_subscriptions',
        to=StoredEventType, verbose_name='Event type'
    )

    objects = EventSubscriptionManager()

    class Meta:
        db_table = 'eventsubscription'
        verbose_name = 'Event subscription'
        verbose_name_plural = 'Event subscriptions'

    def __str__(self):
        return str(self.stored_event_type)


class Notification(NotificationBusinessLogicMixin, models.Model):
    """
    This model keeps track of the notifications for a user. Notifications are
    created when an event to which this user has been subscribed, are
    committed elsewhere in the system.
    """
    user = models.ForeignKey(
        db_index=True, on_delete=models.CASCADE,
        related_name='notifications', to=settings.AUTH_USER_MODEL,
        verbose_name='User'
    )
    action = models.ForeignKey(
        on_delete=models.CASCADE, related_name='notifications', to=Action,
        verbose_name='Action'
    )
    read = models.BooleanField(
        default=False, verbose_name='Read'
    )

    objects = NotificationManager()

    class Meta:
        db_table = 'notification'
        ordering = ('-action__timestamp',)
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'

    def __str__(self):
        return str(self.action)


class ObjectEventSubscription(models.Model):
    content_type = models.ForeignKey(
        on_delete=models.CASCADE, to=ContentType,
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(
        ct_field='content_type',
        fk_field='object_id',
    )
    user = models.ForeignKey(
        db_index=True, on_delete=models.CASCADE,
        related_name='object_subscriptions', to=settings.AUTH_USER_MODEL,
        verbose_name='User'
    )
    stored_event_type = models.ForeignKey(
        on_delete=models.CASCADE, related_name='object_subscriptions',
        to=StoredEventType, verbose_name='Event type'
    )

    objects = ObjectEventSubscriptionManager()

    class Meta:
        db_table = 'objecteventsubscription'
        ordering = ('pk',)
        verbose_name = 'Object event subscription'
        verbose_name_plural = 'Object event subscriptions'

    def __str__(self):
        return str(self.stored_event_type)
