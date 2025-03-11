import logging

from django.apps import AppConfig
from django.contrib import admin

logger = logging.getLogger(name=__name__)


class NPMISAppConfig(AppConfig):
    app_namespace = None

    def ready(self):
        logger.debug('Initializing app: %s', self.name)


class CommonConfig(NPMISAppConfig):
    app_namespace = 'common'
    name = "npmis.apps.common"
    verbose_name = 'Common'

    def ready(self):
        super().ready()

        admin.autodiscover()


