from npmis.apps.events.classes import EventTypeNamespace

namespace = EventTypeNamespace(
    label='Access control lists', name='acls'
)

event_acl_created = namespace.add_event_type(label='ACL created', name='acl_created')
event_acl_deleted = namespace.add_event_type(label='ACL deleted', name='acl_deleted')
event_acl_edited = namespace.add_event_type(label='ACL edited', name='acl_edited')
