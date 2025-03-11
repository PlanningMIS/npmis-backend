import os
import uuid

from django.utils.dateparse import parse_date
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from npmis.apps.settings.serializers import SectorSerializer, ProjectNatureSerializer
from .models import Project, ProjectFunding


class ProjectFundingSerializer(ModelSerializer):
    class Meta:
        model = ProjectFunding
        fields = ['project', 'fund_source', 'fund_category', 'financing_modality', 'financier', 'committed_amount',
                  'currency', 'exchange_rate']


class ConceptNoteCreateSerializer(serializers.ModelSerializer):
    estimated_cost = serializers.CharField()
    concept_note = serializers.FileField(required=False, allow_null=True)  # File handling
    project_fundings = ProjectFundingSerializer(many=True, required=False)  # Accept multiple fundings

    class Meta:
        model = Project
        fields = [
            'project_name', 'programme', 'project_nature', 'project_description', 'project_background',
            'exp_start_date', 'exp_completion_date', 'sector', 'subsector', 'estimated_cost', 'lifespan',
            'project_objective', 'financing_structure', 'project_fundings', 'costcentre', 'concept_note',
        ]

    def validate_estimated_cost(self, value):
        """Ensure estimated cost is a positive number."""
        if not value:
            return 0

        try:
            cleaned_value = float(value.replace(",", ""))
        except ValueError:
            raise serializers.ValidationError("Estimated cost must be a valid number.")

        if cleaned_value <= 0:
            raise serializers.ValidationError("Estimated cost must be a positive number.")

        return cleaned_value

    def validate_concept_note(self, value):
        """Validate and rename the uploaded concept note file."""
        if value:
            # Validate file size (max 5MB)
            if value.size > 5 * 1024 * 1024:
                raise serializers.ValidationError("File size cannot exceed 5MB.")

            # Validate file type (only PDF and Word documents)
            if not value.name.lower().endswith(('.pdf', '.doc', '.docx')):
                raise serializers.ValidationError("Only PDF and Word documents are allowed.")

        return value

    def validate(self, data):
        """Cross-field validation."""
        start_date = parse_date(str(data.get("exp_start_date", "")))
        end_date = parse_date(str(data.get("exp_completion_date", "")))

        if not start_date or not end_date:
            raise serializers.ValidationError({"exp_start_date": "Invalid date format. Use YYYY-MM-DD."})

        if start_date >= end_date:
            raise serializers.ValidationError(
                {"exp_completion_date": "Expected completion date must be after the start date."})

        return data

    def create(self, validated_data):
        """Create a Project along with multiple ProjectFunding entries."""
        project_fundings_data = validated_data.pop('project_fundings', [])
        project = Project.objects.create(**validated_data)

        # Bulk create ProjectFundings
        project_fundings = [
            ProjectFunding(project=project, **funding_data)
            for funding_data in project_fundings_data
        ]
        ProjectFunding.objects.bulk_create(project_fundings)

        return project


class ConceptNoteListSerializer(ModelSerializer):
    sector = SectorSerializer()
    project_nature = ProjectNatureSerializer()

    class Meta:
        model = Project
        fields = [
            'project_id', 'project_name', 'project_nature', 'sector', 'exp_start_date',
            'exp_completion_date', 'estimated_cost', 'status'
        ]


class ConceptNoteSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'project_id', 'project_name', 'programme', 'project_nature', 'project_description', 'project_background',
            'exp_start_date', 'exp_completion_date', 'sector', 'subsector', 'estimated_cost', 'lifespan',
            'project_objective', 'costcentre', 'concept_note',
        ]
