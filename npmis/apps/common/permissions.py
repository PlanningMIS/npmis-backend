from npmis.apps.permissions.classes import PermissionNamespace

namespace = PermissionNamespace(label='Common', name='common')

permission_object_copy = namespace.add_permission(label='Copy object', name='object_copy')
