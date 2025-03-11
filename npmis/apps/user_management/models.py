from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q

from .events import event_user_created
from .managers import UserManager
from npmis.apps.settings.models import Institution, Vote
from ..events.decorators import method_event
from ..events.managers import EventManagerSave


class User(AbstractUser):
    email = models.EmailField('email address', unique=True, null=True, blank=True)
    phone = models.CharField(max_length=30, null=True, blank=True)
    vote = models.ForeignKey(Vote, models.CASCADE, null=True, blank=True, to_field='vote_no')
    institution = models.ForeignKey(Institution, models.CASCADE, null=True, blank=True)
    REQUIRED_FIELDS = ['email', 'phone']

    objects = UserManager()

    class Meta:
        verbose_name = 'User'
        db_table = 'user'
        ordering = ['id']
        constraints = [
            models.UniqueConstraint(
                fields=['email'],
                name='unique_when_not_null',
                condition=Q(email__isnull=False),
            ),
        ]

    def __str__(self):
        """
        Returns a string representation of the User.

        If the user has a first and last name, this will be in the format
        "first_name last_name". Otherwise, it will be the username.
        """
        # If the user has a first and last name, return them
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        # Otherwise, return the username
        return self.username

    # @method_event(
    #     event_manager_class=EventManagerSave,
    #     created={
    #         'action_object': 'self',
    #         'event': event_user_created,
    #         'target': 'self'
    #     }
    # )
    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)
