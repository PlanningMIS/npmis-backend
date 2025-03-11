from django.apps import apps
from django.db.models.signals import post_migrate

from npmis.apps.common.apps import NPMISAppConfig
from npmis.apps.events.classes import EventModelRegistry, ModelEventType
from npmis.apps.acls.classes import ModelPermission
from npmis.apps.acls.permissions import permission_acl_edit, permission_acl_view
from npmis.apps.common.classes import ModelCopy

from .classes import Permission
from .events import event_role_created, event_role_edited
from .handlers import handler_permission_initialize, handler_purge_permissions
from .methods import method_group_roles_add, method_group_roles_remove
from .permissions import permission_role_delete, permission_role_edit, permission_role_view
from ..common.signals import signal_perform_upgrade


class PermissionsConfig(NPMISAppConfig):
    app_namespace = 'permissions'
    name = 'npmis.apps.permissions'
    verbose_name = 'Permissions'

    def ready(self):
        super().ready()

        Role = self.get_model('Role')
        StoredPermission = self.get_model('StoredPermission')
        Group = apps.get_model(app_label='auth', model_name='Group')

        Group.add_to_class(name='roles_add', value=method_group_roles_add)
        Group.add_to_class(name='roles_remove', value=method_group_roles_remove)

        EventModelRegistry.register(model=Role)
        EventModelRegistry.register(model=StoredPermission)
        ModelCopy(
            model=Role, register_permission=True
        ).add_fields(
            field_names=(
                'label', 'permissions', 'groups',
            ),
        )
        ModelCopy.add_fields_lazy(
            model=Group, field_names=(
                'roles',
            ),
        )

        ModelEventType.register(
            event_types=(event_role_created, event_role_edited), model=Role
        )

        ModelPermission.register(
            model=Role, permissions=(
                permission_acl_edit, permission_acl_view,
                permission_role_delete, permission_role_edit,
                permission_role_view
            )
        )

        # Initialize the permissions at the ready method for subsequent
        # restarts.
        Permission.load_modules()

        # Initialize the permissions post migrate of this app for new
        # installations
        post_migrate.connect(
            dispatch_uid='permissions_handler_permission_initialize',
            receiver=handler_permission_initialize,
            sender=self
        )
        signal_perform_upgrade.connect(
            dispatch_uid='permissions_handler_purge_permissions',
            receiver=handler_purge_permissions
        )

