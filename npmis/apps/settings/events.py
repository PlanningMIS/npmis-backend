
from npmis.apps.events.classes import EventTypeNamespace

namespace = EventTypeNamespace(
    label='Settings', name='settings'
)

event_sdg_created = namespace.add_event_type(
    label='SDG created', name='sdg_create'
)
event_sdg_edited = namespace.add_event_type(
    label='SDG edited', name='sdg_edit'
)
event_sdg_viewed = namespace.add_event_type(
    label='SDG viewed', name='sdg_view'
)
event_sdg_deleted = namespace.add_event_type(
    label='SDG deleted', name='sdg_delete'
)