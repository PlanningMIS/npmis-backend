import logging

from django.db import transaction
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.generics import UpdateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response


from npmis.apps.common.classes import Response
from .filters import ProjectFilter
from .models import Project
from .serializers import ConceptNoteCreateSerializer, ConceptNoteSerializer, ConceptNoteListSerializer

logger = logging.getLogger(__name__)


class ConceptNoteListAPIView(ListAPIView):
    """
    This view will list all projects with project_no set to None.
    A project with project_no set to None is considered a concept note.
    This view will return a list of such projects.
    """
    queryset = Project.objects.filter(project_no__isnull=True)
    serializer_class = ConceptNoteListSerializer
    filterset_class = ProjectFilter

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        try:
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            else:
                serializer = self.get_serializer(queryset, many=True)
                return Response(
                    status_code=status.HTTP_200_OK,
                    data=serializer.data
                )
        except Exception as e:
            return Response(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message=f"{e}",
            )


class ConceptNoteCreateAPIView(CreateAPIView):
    queryset = Project.objects.filter(project_no__isnull=True)
    serializer_class = ConceptNoteCreateSerializer
    parser_classes = (MultiPartParser, FormParser)  # Allow file uploads

    def create(self, request, *args, **kwargs):
        # Extract extra data
        extra_data = {'vote': request.user.vote}

        # Merge request data and files
        request_data = request.data.copy()
        request_data.update(extra_data)

        # Include file if present
        files = request.FILES if 'concept_note' in request.FILES else None

        # Initialize the serializer
        serializer = self.serializer_class(data=request_data, files=files, context={'request': request})

        try:
            with transaction.atomic():
                if serializer.is_valid():
                    serializer.save()
                    return Response(
                        message="Concept note submitted successfully",
                        status_code=status.HTTP_201_CREATED
                    )
                else:
                    return Response(
                        message="Validation error occurred",
                        status_code=status.HTTP_400_BAD_REQUEST
                    )
        except Exception as e:
            logger.error(f'Error submitting concept note: {e}')
            return Response(
                message="An error occurred while submitting the concept note",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ConceptNoteUpdateAPIView(UpdateAPIView):
    queryset = Project.objects.filter(project_no__isnull=True)
    serializer_class = ConceptNoteSerializer


class ConceptNoteDetailAPIView(RetrieveAPIView):
    queryset = Project.objects.filter(project_no__isnull=True)
    serializer_class = ConceptNoteSerializer
