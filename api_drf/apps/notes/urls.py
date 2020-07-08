from django.urls import path
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from .views import NoteCreateView, NoteListViewAsCreator,\
    CategoryDetailView, CategoryListView, CategoryCreateView, NoteDetailViewCreator,\
    NoteDetailViewEditor, UserListView, NoteListViewAsEditor
from . import views

urlpatterns = [
    path('category/create/', CategoryCreateView.as_view()),
    path('category/detail/<int:pk>', CategoryDetailView.as_view()),
    path('category/all/', CategoryListView.as_view()),
    path('note/create/', NoteCreateView.as_view()),
    path('note/all/as_creator/', NoteListViewAsCreator.as_view()),
    path('note/all/as_editor/', NoteListViewAsEditor.as_view()),
    path('users/all/', UserListView.as_view()),
    path('note/detail/<int:pk>/creator', NoteDetailViewCreator.as_view()),
    path('note/detail/<int:pk>/editor', NoteDetailViewEditor.as_view()),

]