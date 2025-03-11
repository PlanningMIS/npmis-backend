from django.db import models
from django.db.models import Q
from django_filters import rest_framework as filters

from npmis.apps.projects.models import Project


class ProjectFilter(filters.FilterSet):
    project_name = filters.CharFilter(method='filter_by_name_or_reference')

    class Meta:
        model = Project
        fields = [
            'project_name', 'project_nature', 'sector', 'status'
        ]

    def filter_by_name_or_reference(self, queryset, project_name, value):
        return queryset.filter(
            Q(project_name__icontains=value) | Q(project_id__icontains=value)
        )
