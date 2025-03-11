
from npmis.apps.permissions.classes import PermissionNamespace

namespace = PermissionNamespace(label='User management', name='user_management')

permission_group_create = namespace.add_permission(label='Create new groups', name='group_create')
permission_group_delete = namespace.add_permission(label='Delete existing groups', name='group_delete')
permission_group_edit = namespace.add_permission(label='Edit existing groups', name='group_edit')
permission_group_view = namespace.add_permission(label='View existing groups', name='group_view')
permission_user_create = namespace.add_permission(label='Create new users', name='user_create')
permission_user_delete = namespace.add_permission(label='Delete existing users', name='user_delete')
permission_user_edit = namespace.add_permission(label='Edit existing users', name='user_edit')
permission_user_view = namespace.add_permission(label='View existing users', name='user_view')
