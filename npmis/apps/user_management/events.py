from npmis.apps.events.classes import EventTypeNamespace

namespace = EventTypeNamespace(
    label='User management', name='user_management'
)

event_user_created = namespace.add_event_type(label='User created', name='user_created')
event_user_deleted = namespace.add_event_type(label='User deleted', name='user_deleted')
event_user_edited = namespace.add_event_type(label='User edited', name='user_edited')
