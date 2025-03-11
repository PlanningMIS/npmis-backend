from django.apps import apps
from django.db import models
from npmis.apps.common.apps import NPMISAppConfig
from npmis.apps.acls.classes import ModelPermission

from .classes import EventTypeNamespace


class EventsConfig(NPMISAppConfig):
    app_namespace = 'events'
    name = 'npmis.apps.events'
    verbose_name = 'Events'

    def ready(self):
        super().ready()

        Action = apps.get_model(app_label='actstream', model_name='Action')
        Notification = apps.get_model(app_label='events', model_name='Notification')
        ObjectEventSubscription = apps.get_model(app_label='events', model_name='ObjectEventSubscription')

        EventTypeNamespace.load_modules()

        ModelPermission.register_inheritance(fk_field_cast=models.CharField, model=Action, related='action_object')
        ModelPermission.register_inheritance(fk_field_cast=models.CharField, model=Action, related='actor')
        ModelPermission.register_inheritance(fk_field_cast=models.CharField, model=Action, related='target')

        ModelPermission.register_inheritance(fk_field_cast=models.CharField, model=Notification, related='action__action_object')
        ModelPermission.register_inheritance(fk_field_cast=models.CharField, model=Notification, related='action__actor')
        ModelPermission.register_inheritance(fk_field_cast=models.CharField, model=Notification, related='action__target')

        ModelPermission.register_inheritance(fk_field_cast=models.CharField, model=ObjectEventSubscription, related='content_object')

