from django.apps import AppConfig

from npmis.apps.acls.classes import ModelPermission
from npmis.apps.acls.permissions import permission_acl_edit, permission_acl_view
from npmis.apps.common.apps import NPMISAppConfig
from npmis.apps.common.classes import ModelCopy
from npmis.apps.events.classes import EventModelRegistry, ModelEventType
from npmis.apps.settings.events import event_sdg_edited, event_sdg_created, event_sdg_deleted
from npmis.apps.settings.permissions import permission_sdg_edit, permission_sdg_view


class SettingsConfig(NPMISAppConfig):
    app_namespace = 'settings'
    name = "npmis.apps.settings"
    verbose_name = 'Settings'

    def ready(self):
        super().ready()

        Sdg = self.get_model(model_name='Sdg')
        SdgGoal = self.get_model(model_name='SdgGoal')
        SdgTarget = self.get_model(model_name='SdgTarget')

        EventModelRegistry.register(model=Sdg)
        EventModelRegistry.register(model=SdgGoal)
        EventModelRegistry.register(model=SdgTarget)

        ModelCopy(model=Sdg, register_permission=True).add_fields(
            field_names=(
                'id', 'name', 'description', 'start_date', 'end_date', 'is_active'
            )
        )

        ModelEventType.register(
            model=Sdg, event_types=(
                event_sdg_edited, event_sdg_created, event_sdg_deleted
            )
        )
        ModelPermission.register(
            model=Sdg, permissions=(
                permission_acl_edit, permission_acl_view,
                permission_sdg_edit, permission_sdg_view
            )
        )
