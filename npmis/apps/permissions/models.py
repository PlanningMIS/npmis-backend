from django.contrib.auth.models import Group
from django.db import models

from npmis.apps.events.decorators import method_event
from npmis.apps.events.managers import EventManagerSave

from .events import event_role_edited, event_role_created
from .mixins import RoleBusinessLogicMixin, StoredPermissionBusinessLogicMixin
from .managers import RoleManager, StoredPermissionManager


class Role(RoleBusinessLogicMixin, models.Model):
    """
    This model represents a Role. Roles are permission units. They are the
    only object to which permissions can be granted. They are themselves
    containers too, containing Groups, which are organization units. Roles
    are the basic method to grant a permission to a group. Permissions granted
    to a group using a role, are granted for the entire system.
    """
    label = models.CharField(
        help_text='A short text describing the role.',
        max_length=128, unique=True, verbose_name='Label'
    )
    permissions = models.ManyToManyField(
        related_name='roles', to='StoredPermission',
        verbose_name='Permissions'
    )
    groups = models.ManyToManyField(
        related_name='roles', to=Group, verbose_name='Groups'
    )

    objects = RoleManager()

    class Meta:
        db_table = 'role'
        ordering = ('label',)
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'

    def __init__(self, *args, **kwargs):
        _instance_extra_data = kwargs.pop(
            '_instance_extra_data', {}
        )
        result = super().__init__(*args, **kwargs)
        for key, value in _instance_extra_data.items():
            setattr(self, key, value)

        return result

    def __str__(self):
        return self.label

    def natural_key(self):
        return (self.label,)

    natural_key.dependencies = ['auth.Group', 'permissions.StoredPermission']

    @method_event(
        event_manager_class=EventManagerSave,
        created={
            'event': event_role_created,
            'target': 'self',
        },
        edited={
            'event': event_role_edited,
            'target': 'self',
        }
    )
    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)


class StoredPermission(StoredPermissionBusinessLogicMixin, models.Model):
    """
    This model is the counterpart of the permissions.classes.Permission
    class. Allows storing a database counterpart of a permission class.
    It is used to store the permissions help by a role or in an ACL.
    """
    namespace = models.CharField(
        max_length=64, verbose_name='Namespace'
    )
    name = models.CharField(
        max_length=64, verbose_name='Name'
    )

    objects = StoredPermissionManager()

    class Meta:
        db_table = 'storedpermission'
        ordering = ('namespace',)
        unique_together = ('namespace', 'name')
        verbose_name = 'Permission'
        verbose_name_plural = 'Permissions'

    def __str__(self):
        return str(self.label)

    def natural_key(self):
        return self.namespace, self.name
