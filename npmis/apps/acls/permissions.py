from npmis.apps.permissions.classes import PermissionNamespace

namespace = PermissionNamespace(label='Access control lists', name='acls')

permission_acl_edit = namespace.add_permission(label='Edit ACLs', name='acl_edit')
permission_acl_view = namespace.add_permission(label='View ACLs', name='acl_view')
