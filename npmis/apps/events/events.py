from django.utils.translation import gettext_lazy as _

from npmis.apps.events.classes import EventTypeNamespace

from .literals import (
    EVENT_EVENTS_CLEARED_NAME,
    EVENT_TYPE_NAMESPACE_NAME
)

namespace = EventTypeNamespace(
    label='Events', name=EVENT_TYPE_NAMESPACE_NAME
)

event_events_cleared = namespace.add_event_type(
    label='Events cleared', name=EVENT_EVENTS_CLEARED_NAME
)

