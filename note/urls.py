from django.urls import path
from .views import (
    NoteCreateListView,NoteDetailUpdateDeleteView,NoteIsNotEnableListView
)

urlpatterns = [
    path('note/',NoteCreateListView.as_view(),name='note-list'),
    path('note/<int:pk>/',NoteDetailUpdateDeleteView.as_view(),name='note-detail'),
    path('note/not_enable/',NoteIsNotEnableListView.as_view(),name='note-not-enable'),
]