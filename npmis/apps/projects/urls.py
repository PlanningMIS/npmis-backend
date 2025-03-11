from django.urls import path

from .views import ConceptNoteCreateAPIView, ConceptNoteListAPIView, ConceptNoteUpdateAPIView, ConceptNoteDetailAPIView

urlpatterns = [
    path('conceptnote/', ConceptNoteListAPIView.as_view(), name='list_conceptnotes'),
    path('conceptnote/create', ConceptNoteCreateAPIView.as_view(), name='create_conceptnote'),
    path('conceptnote/update/<str:pk>', ConceptNoteUpdateAPIView.as_view(), name='update_conceptnote'),
    path('conceptnote/detail/<str:pk>', ConceptNoteDetailAPIView.as_view(), name='detail_conceptnote'),
]