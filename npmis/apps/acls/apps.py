from npmis.apps.common.apps import NPMISAppConfig
from npmis.apps.common.classes import ModelCopy
from npmis.apps.events.classes import EventModelRegistry, ModelEventType

from .classes import ModelPermission
from .events import event_acl_deleted, event_acl_edited


class AclsConfig(NPMISAppConfig):
    app_namespace = 'acls'
    name = 'npmis.apps.acls'
    verbose_name = 'ACLs'

    def ready(self):
        super().ready()

        AccessControlList = self.get_model(model_name='AccessControlList')
        self.get_model(
            model_name='GlobalAccessControlListProxy'
        )
        EventModelRegistry.register(model=AccessControlList)

        ModelCopy(model=AccessControlList).add_fields(
            field_names=(
                'content_object', 'permissions', 'role'
            )
        )

        ModelEventType.register(
            event_types=(
                event_acl_deleted, event_acl_edited
            ), model=AccessControlList
        )

        ModelPermission.register_inheritance(
            model=AccessControlList, related='content_object',
        )


