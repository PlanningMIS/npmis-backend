import logging

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

from npmis.apps.events.decorators import method_event
from npmis.apps.events.managers import EventManagerMethodAfter, EventManagerSave
from npmis.apps.permissions.models import Role, StoredPermission

from .events import event_acl_created, event_acl_deleted
from .managers import AccessControlListManager
from .mixins import AccessControlListBusinessLogicMixin

logger = logging.getLogger(name=__name__)


class AccessControlList(AccessControlListBusinessLogicMixin, models.Model):
    """
    ACL means Access Control List it is a more fine-grained method of
    granting access to objects. In the case of ACLs, they grant access using
    3 elements: actor, permission, object. In this case the actor is the role,
    the permission is the Mayan permission and the object can be anything:
    a document, a folder, an index, etc. This means = "Grant X permissions
    to role Y for object Z". This model holds the permission, object, actor
    relationship for one access control list.
    Fields:
    * Role - Custom role that is being granted a permission. Roles are created
    in the Setup menu.
    """
    content_type = models.ForeignKey(
        on_delete=models.CASCADE, related_name='object_content_type',
        to=ContentType, verbose_name=_(message='Content type')
    )
    object_id = models.PositiveIntegerField(
        verbose_name=_(message='Object ID')
    )
    content_object = GenericForeignKey(
        ct_field='content_type', fk_field='object_id'
    )
    permissions = models.ManyToManyField(
        blank=True, related_name='acls', to=StoredPermission,
        verbose_name=_(message='Permissions')
    )
    role = models.ForeignKey(
        help_text=_(
            'Role to which the access is granted for the specified object.'
        ), on_delete=models.CASCADE, related_name='acls', to=Role,
        verbose_name=_(message='Role')
    )

    objects = AccessControlListManager()

    class Meta:
        db_table = 'accesscontrolist'
        ordering = ('pk',)
        unique_together = ('content_type', 'object_id', 'role')
        verbose_name = _(message='Access entry')
        verbose_name_plural = _(message='Access entries')

    def __str__(self):
        return 'Role "%(role)s" permission\'s for "%(object)s"' % {
            'object': self.content_object,
            'role': self.role
        }

    @method_event(
        event_manager_class=EventManagerMethodAfter,
        event=event_acl_deleted,
        target='content_object'
    )
    def delete(self, *args, **kwargs):
        return super().delete(*args, **kwargs)

    @method_event(
        event_manager_class=EventManagerSave,
        created={
            'action_object': 'content_object',
            'event': event_acl_created,
            'target': 'self'
        }
    )
    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)


class GlobalAccessControlListProxy(AccessControlList):
    class Meta:
        proxy = True
