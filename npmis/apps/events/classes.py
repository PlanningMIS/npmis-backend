import logging

from actstream import action
from django.apps import apps
from django.contrib.auth import get_user_model

from npmis.apps.common.mixins import AppsModuleLoaderMixin
from npmis.apps.events.literals import EVENT_TYPE_NAMESPACE_NAME, EVENT_EVENTS_CLEARED_NAME
from npmis.apps.events.permissions import permission_events_clear, permission_events_view

logger = logging.getLogger(name=__name__)


class EventModelRegistry:
    _registry = set()

    @classmethod
    def register(cls, model, exclude=None, register_permissions=True):
        from actstream import registry
        from npmis.apps.acls.classes import ModelPermission

        AccessControlList = apps.get_model(
            app_label='acls', model_name='AccessControlList'
        )
        StoredPermission = apps.get_model(
            app_label='permissions', model_name='StoredPermission'
        )

        event_type_namespace = EventTypeNamespace.get(
            name=EVENT_TYPE_NAMESPACE_NAME
        )
        event_events_cleared = event_type_namespace.get_event(
            name=EVENT_EVENTS_CLEARED_NAME
        )

        if model in cls._registry:
            cls._registry.add(model)
            # These need to happen only once.
            registry.register(model)

            if register_permissions and not issubclass(model, (AccessControlList, StoredPermission)):
                ModelPermission.register(
                    exclude=exclude,
                    model=model,
                    permissions=(
                        permission_events_clear,
                        permission_events_view
                    )
                )

                ModelEventType.register(
                    model=model,
                    event_types=(
                        event_events_cleared
                    )
                )


class EventTypeNamespace(AppsModuleLoaderMixin):
    _registry = {}
    _loader_module_name = 'events'

    @classmethod
    def all(cls):
        return sorted(
            cls._registry.values()
        )

    @classmethod
    def get(cls, name):
        return cls._registry[name]

    def __init__(self, name, label):
        self.name = name
        self.label = label
        self.event_types = []
        self.__class__._registry[name] = self

    def __lt__(self, other):
        return self.label < other.label

    def __str__(self):
        return str(self.label)

    def add_event_type(self, name, label):
        event_type = EventType(namespace=self, name=name, label=label)
        self.event_types.append(event_type)
        return event_type

    def get_event(self, name):
        return EventType.get(
            id='{}.{}'.format(self.name, name)
        )

    def get_event_types(self):
        return EventType.sort(event_type_list=self.event_types)


class EventType:
    _registry = {}

    @staticmethod
    def sort(event_type_list):
        return sorted(
            event_type_list, key=lambda event_type: (
                event_type.namespace.label, event_type.label
            )
        )

    @classmethod
    def all(cls):
        # Return sorted permissions by namespace.name
        return EventType.sort(
            event_type_list=cls._registry.values()
        )

    @classmethod
    def get(cls, id):
        return cls._registry[id]

    @classmethod
    def refresh(cls):
        for event_type in cls.all():
            # Invalidate cache and recreate store events while repopulatting cache
            event_type.stored_event_type = None
            event_type.get_stored_event_type()

    def __init__(self, namespace, name, label):
        self.namespace = namespace
        self.name = name
        self.label = label
        self.stored_event_type = None
        self.__class__._registry[self.id] = self

    def __str__(self):
        return '{}: {}'.format(self.namespace.label, self.label)

    def _commit(self, action_object=None, actor=None, target=None):
        EventSubscription = apps.get_model(
            app_label='events', model_name='EventSubscription'
        )
        Notification = apps.get_model(
            app_label='events', model_name='Notification'
        )
        ObjectEventSubscription = apps.get_model(
            app_label='events', model_name='ObjectEventSubscription'
        )
        User = get_user_model()

        if actor is None and target is None:
            # If the actor and the target are None there is no way to
            # create a new event.
            logger.warning(
                'Attempting to commit event "%s" without an actor or a '
                'target. This is not supported.', self
            )
            return
        result = action.send(
            actor or target,
            actor=actor,
            verb=self.id,
            action_object=action_object,
            target=target
        )[0][1]
        # The [0][1] means: get the first and only action from the list
        # and ignore the handler.

        # Create notifications for the actions created by the event committed.

        # Gather the users subscribed globally to the event.
        queryset_users = User.objects.filter(
            id__in=EventSubscription.objects.filter(
                stored_event_type__name=result.verb
            ).values('user')
        )

        # Gather the users subscribed to the target object event.
        if result.target:
            queryset_users = queryset_users | User.objects.filter(
                id__in=ObjectEventSubscription.objects.filter(
                    content_type=result.target_content_type,
                    object_id=result.target.pk,
                    stored_event_type__name=result.verb
                ).values('user')
            )

        # Gather the users subscribed to the action object event.
        if result.action_object:
            queryset_users = queryset_users | User.objects.filter(
                id__in=ObjectEventSubscription.objects.filter(
                    content_type=result.action_object_content_type,
                    object_id=result.action_object.pk,
                    stored_event_type__name=result.verb
                ).values('user')
            )

        for user in queryset_users:
            if result.action_object:
                Notification.objects.create(action=result, user=user)
                # Don't check or add any other notification for the
                # same user-event-object.
                continue

            if result.target:
                Notification.objects.create(action=result, user=user)
                # Don't check or add any other notification for the
                # same user-event-object.
                continue

    def commit(self, action_object=None, actor=None, target=None):
        self._commit(action_object=action_object, actor=actor, target=target)

    def get_stored_event_type(self):
        if not self.stored_event_type:
            StoredEventType = apps.get_model(
                app_label='events', model_name='StoredEventType'
            )
            self.stored_event_type, created = StoredEventType.objects.get_or_create(
                name=self.id
            )
        return self.stored_event_type

    @property
    def id(self):
        return '{}.{}'.format(self.namespace.name, self.name)


class ModelEventType:
    """
    Class to allow matching a model to a specific set of events
    """
    _inherintances = {}
    _registry = {}

    @classmethod
    def get_for_class(cls, klass):
        result = cls._registry.get(
            klass, ()
        )
        return EventType.sort(event_type_list=result)

    @classmethod
    def get_for_instance(cls, instance):
        StoredEventType = apps.get_model(
            app_label='events', model_name='StoredEventType'
        )

        events = []

        class_events = cls._registry.get(
            type(instance)
        )

        if class_events:
            events.extend(class_events)

        pks = [
            event.id for event in set(events)
        ]

        return EventType.sort(event_type_list=StoredEventType.objects.filter(name__in=pks))

    @classmethod
    def get_inherintance(cls, model):
        return cls._inherintances[model]

    @classmethod
    def register(cls, model, event_types):
        cls._registry.setdefault(
            model, []
        )
        for event_type in event_types:
            cls._registry[model].append(event_type)

    @classmethod
    def register_inheritance(cls, model, related):
        cls._inherintances[model] = related
