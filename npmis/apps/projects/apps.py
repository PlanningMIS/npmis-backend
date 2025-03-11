from npmis.apps.common.apps import NPMISAppConfig


class ProjectsConfig(NPMISAppConfig):
    app_namespace = 'projects'
    name = "npmis.apps.projects"
    verbose_name = 'Projects'

    def ready(self):
        super().ready()

