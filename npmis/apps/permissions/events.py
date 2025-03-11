from npmis.apps.events.classes import EventTypeNamespace

namespace = EventTypeNamespace(label='Permissions', name='permissions')

event_role_created = namespace.add_event_type(label='Role created', name='role_created')
event_role_edited = namespace.add_event_type(label='Role edited', name='role_edited')
