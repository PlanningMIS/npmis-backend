import itertools
import logging

from django.apps import apps
from django.core.exceptions import ImproperlyConfigured

from .events import event_acl_created, event_acl_deleted, event_acl_edited
from ..common.utils import get_related_field

logger = logging.getLogger(name=__name__)


class ModelPermission:
    _field_query_functions = {}
    _inheritances = {}
    _inheritances_reverse = {}
    _manager_names = {}
    _model_permissions = {}

    @classmethod
    def deregister(cls, model):
        cls._model_permissions.pop(model, None)

    @classmethod
    def get_choices_for_class(cls, klass):
        result = []

        for namespace, permissions in itertools.groupby(cls.get_for_class(klass=klass), lambda entry: entry.namespace):
            permission_options = [
                (permission.pk, str(permission)) for permission in permissions
            ]
            permission_options.sort(
                key=lambda entry: entry[1]
            )
            result.append((namespace, permission_options))

        # Sort by namespace label.
        result.sort(
            key=lambda entry: entry[0].label
        )
        return result

    @classmethod
    def get_classes(cls, as_content_type=False):
        ContentType = apps.get_model(
            app_label='contenttypes', model_name='ContentType'
        )

        if as_content_type:
            # This returns a dictionary but a queryset is needed.
            content_type_dictionary = ContentType.objects.get_for_models(
                *cls._model_permissions.keys()
            )

            # Convert the dictionary into a list of IDs.
            content_type_ids = [
                content_type.pk for content_type in content_type_dictionary.values()
            ]

            # Return a queryset of content types based on the ID list.
            return ContentType.objects.filter(pk__in=content_type_ids)
        else:
            return cls._model_permissions.keys()

    @classmethod
    def get_field_query_function(cls, model):
        return cls._field_query_functions[model]

    @classmethod
    def get_for_class(cls, klass):
        # Return the permissions for the klass and the models that
        # inherit from it.
        result = set()
        result.update(
            cls._model_permissions.get(
                klass, ()
            )
        )

        for model in cls._inheritances_reverse.get(klass, ()):
            result.update(
                cls._model_permissions.get(
                    model, ()
                )
            )

        result = list(result)
        result.sort(key=lambda permission: permission.namespace.name)

        return result

    @classmethod
    def get_for_instance(cls, instance):
        StoredPermission = apps.get_model(
            app_label='permissions', model_name='StoredPermission'
        )

        permissions = []

        class_permissions = cls.get_for_class(klass=type(instance))

        if class_permissions:
            permissions.extend(class_permissions)

        pks = [permission.stored_permission.pk for permission in set(permissions)]

        return StoredPermission.objects.filter(pk__in=pks)

    @classmethod
    def get_inheritances(cls,model):
        # Proxy models get the inheritance from their base model.
        if model._meta.proxy:
            model = model._meta.proxy_for_model

        return cls._inheritances[model]

    @classmethod
    def get_manager(cls, model):
        try:
            manager_name = cls.get_manager_name(model=model)
        except KeyError:
            manager_name = None

        if manager_name:
            manager = model._meta.default_manager

        return manager

    @classmethod
    def register(cls, model, permissions, exclude=None):
        """
        Match a model class to a set of permissions. And connect the model
        to the ACLs via a GenericRelation field.
        """
        from django.contrib.contenttypes.fields import GenericRelation

        from npmis.apps.common.classes import ModelCopy
        from npmis.apps.events.classes import EventModelRegistry, ModelEventType

        AccessControlList = apps.get_model(app_label='acls', model_name='AccessControlList')
        StoredPermission = apps.get_model(app_label='permissions', model_name='StoredPermission')

        initialize_model_for_events = model not in cls._model_permissions
        is_excluded_subclass = issubclass(
            model, (AccessControlList, StoredPermission)
        )

        cls._model_permissions.setdefault(
            model, set()
        )

        if not is_excluded_subclass:
            try:
                cls._model_permissions[model].update(permissions)
            except TypeError as exception:
                raise ImproperlyConfigured(
                    'Make sure the permissions argument to the .register() '
                    'method is an iterable. Current value: "{}"'.format(
                        permissions
                    )
                ) from exception
        if initialize_model_for_events:
            # These need to happen only once.

            # Allow the model to be used as the action_object for the ACL
            # events.
            EventModelRegistry.register(model=model)

            if not is_excluded_subclass:
                ModelEventType.register(
                    event_types=(
                        event_acl_created, event_acl_deleted,
                        event_acl_edited
                    ), model=model
                )

                model.add_to_class(
                    name='acls', value=GenericRelation(
                        to=AccessControlList, verbose_name='ACLs'
                    )
                )

                ModelCopy.add_fields_lazy(
                    model=model, field_names=('acls')
                )
    @classmethod
    def register_field_query_function(cls, model, function):
        cls._field_query_functions[model] = function

    @classmethod
    def register_inheritance(cls, model, related, fk_field_cast=None):
        model_reverse = get_related_field(
            model=model, related_field_name=related
        ).related_model
        cls._inheritances_reverse.setdefault(
            model_reverse, []
        )
        cls._inheritances_reverse[model_reverse].append(model)

        cls._inheritances.setdefault(
            model, []
        )
        cls._inheritances[model].append(
            {'field_name': related, 'fk_field_cast': fk_field_cast}
        )

    @classmethod
    def register_manager(cls, model, manager_name):
        cls._manager_names[model] = manager_name


