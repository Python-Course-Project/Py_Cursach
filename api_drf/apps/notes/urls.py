from django.urls import path
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from .views import NoteCreateView, NoteListView,\
    CategoryDetailView, CategoryListView, CategoryCreateView, NoteDetailViewCreator,\
    NoteDetailViewEditor
from . import views

urlpatterns = [
    path('category/create/', CategoryCreateView.as_view()),
    path('category/detail/<int:pk>', CategoryDetailView.as_view()),
    path('category/all/', CategoryListView.as_view()),
    path('note/create/', NoteCreateView.as_view()),
    path('note/all/', NoteListView.as_view()),
    path('note/detail/<int:pk>/creator', NoteDetailViewCreator.as_view()),
    path('note/detail/<int:pk>/editor', NoteDetailViewEditor.as_view()),

]