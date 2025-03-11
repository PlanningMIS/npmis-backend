from importlib import import_module
import logging

from django.apps import apps

logger = logging.getLogger(name=__name__)


class AppsModuleLoaderMixin:
    __loader_module_sets = {}
    __loader_module_name = None

    @classmethod
    def load_modules(cls):
        cls.__loader_module_sets.setdefault(
            cls.__loader_module_name, set()
        )

        for app in apps.get_app_configs():
            if app not in cls.__loader_module_sets[cls.__loader_module_name]:
                try:
                    import_module(
                        name='{}.{}'.format(
                            app.name, cls.__loader_module_name
                        )
                    )
                except ImportError as exception:
                    non_fatal_messages = (
                        'No module named {module_name}'.format(
                            module_name=cls.__loader_module_name
                        ),
                        'No module named \'{app_lable}.{module_name}\''.format(
                            app_lable=app.name,
                            module_name=cls.__loader_module_name
                        )
                    )
                    if str(exception) not in non_fatal_messages:
                        logger.error(
                            'Error importing %s %s.py file; %s', app.name,
                            cls._loader_module_name, exception, exc_info=True
                        )
                        raise
                finally:
                    cls.__loader_module_sets[cls.__loader_module_name].add(app)
        cls.post_load_modules(cls)

    @classmethod
    def post_load_modules(cls):
        return
