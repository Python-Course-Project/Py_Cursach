from django.urls import path
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from .views import NoteCreateView, NoteListView,\
    CategoriaDetailView, CategoriaListView, CategoriaCreateView, NoteDetailViewCreator,\
    NoteDetailViewEditor
#from .views import login_view, logout_view, register_view
from . import views

# router = DefaultRouter()
# router.register(r'notes', NoteViewSet, basename='user')
# router.register(r'user', UserViewSet, basename='login')
# # router.register(r'^logout', logout_view, basename='logout')
# # router.register(r'^sign_up', register_view, basename='register')
# urlpatterns = router.urls
# app_name = 'notes
urlpatterns = [
    path('categoria/create/', CategoriaCreateView.as_view()),
    path('categoria/detail/<int:pk>', CategoriaDetailView.as_view()),
    path('categoria/all/', CategoriaListView.as_view()),
    path('note/create/', NoteCreateView.as_view()),
    path('note/all/', NoteListView.as_view()),
   # path('note/detail/<int:pk>', NoteDetailView.as_view()),
    path('note/detail/<int:pk>/creator', NoteDetailViewCreator.as_view()),
    path('note/detail/<int:pk>/editor', NoteDetailViewEditor.as_view()),

]