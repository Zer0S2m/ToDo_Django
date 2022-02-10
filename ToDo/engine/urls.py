from django.urls import path

from .views import (
	NoteListView, NoteDetailView, CategoryDetailView,
	CategoryListView, NoteDeleteView, NoteUpdateView,
	NoteCreateView, CategoryCreateView, CategoryDeleteView,
	CategoryUpdateView, NoteCompleteView
)


urlpatterns = [
	path('', NoteListView.as_view(), name = 'list_note'),
	path('note/create/', NoteCreateView.as_view(), name = "create_note"),
	path('note/<int:pk>/', NoteDetailView.as_view(), name = 'detail_note'),
	path('note/delete/<int:pk>/', NoteDeleteView.as_view(), name = 'delete_note'),
	path('note/complete/<int:pk>/', NoteCompleteView.as_view(), name = 'complete_name'),
	path('note/edit/<int:pk>/', NoteUpdateView.as_view(), name = 'edit_note'),

	path('category/', CategoryListView.as_view(), name = 'list_category'),
	path('category/create/', CategoryCreateView.as_view(), name = 'create_category'),
	path('category/<slug:slug>/', CategoryDetailView.as_view(), name = 'detail_category'),
	path('category/delete/<slug:slug>/', CategoryDeleteView.as_view(), name = 'delete_category'),
	path('category/edit/<slug:slug>/', CategoryUpdateView.as_view(), name = 'edit_category'),
]
