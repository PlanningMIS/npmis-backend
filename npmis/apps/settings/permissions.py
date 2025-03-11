from django.utils.translation import gettext_lazy as _

from npmis.apps.permissions.classes import PermissionNamespace

namespace = PermissionNamespace(
    label='Settings', name='settings'
)

permission_sdg_create = namespace.add_permission(
    label='Create SDG', name='sdg_create'
)
permission_sdg_edit = namespace.add_permission(
    label=_(message='Edit SDG'), name='sdg_edit'
)

permission_sdg_view = namespace.add_permission(
    label=_(message='View SDGs'), name='sdg_view'
)
