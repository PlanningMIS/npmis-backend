from npmis.apps.permissions.classes import PermissionNamespace

namespace = PermissionNamespace(label='Events', name='events')

permission_events_clear = namespace.add_permission(label='Clear the events of an object', name='events_clear')
permission_events_view = namespace.add_permission(label='View the events of an object', name='events_view')
