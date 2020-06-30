from django.http import HttpResponse
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .permissions import IsCreater, IsCreaterNote, IsEditorNote
from rest_framework.permissions import IsAuthenticated
from .models import Note, Categoria
from .serializers import SecontNoteDetailSeril,\
    SecontNoteListSeril,\
    CategoriaListSeril,\
    CategoriaDetailSeril,\
    CreateNoteSeril,\
    NoteDetailSerilEditor,\
    full_serial, CategoriaSchema
from functools import partial
from rest_framework import filters
from django.db.models import Q
from .service import get_client_ip
from django.contrib.auth import get_user_model
User = get_user_model()
from django.db import models

"""
Категории
"""
class CategoriaCreateView(generics.CreateAPIView):
    serializer_class = CategoriaDetailSeril
    queryset = Categoria.objects.all()
    permission_classes = (IsAuthenticated, IsCreater)

    # def post(self, request, *args, **kwargs):
    #     data = request.data
    #     serializer = self.serializer_class(data=data)
    #     serializer.is_valid(raise_exception=True)
    #     self.request['my_note_isadded'] = True
    #    # return self.create(request, *args, **kwargs)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)

    
    # def get_queryset(self):
    #     my_note = Note.objects.annotate(
    #         isadded_user=models.Count("notes", filter=models.Q(notes__creator=self.request.user))
    #     )
    #     return my_note

class CategoriaListView(generics.ListAPIView):
    serializer_class = CategoriaListSeril
    queryset = Categoria.objects.all() #Говоряит о том, какие записи мы хотим вынуть
    permission_classes = (IsAuthenticated, IsCreater)
    # """
    # Переопределение этого метода позволяет настроить набор запросов,
    #  возвращаемый представлением, несколькими различными способами.
    # """
    def get_queryset(self):
        return self.queryset.filter(creator=self.request.user)

class CategoriaDetailView(generics.RetrieveUpdateDestroyAPIView): #позволяет обновлять получать удалять данные об одном объекте
    serializer_class = CategoriaDetailSeril
    queryset = Categoria.objects.all()
    permission_classes = (IsCreater, IsAuthenticated, )


"""
Создание заметки
"""
class NoteCreateView(generics.CreateAPIView):
    serializer_class = CreateNoteSeril
    permission_classes = (IsAuthenticated, )
    queryset = Note.objects.all()
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['=editor_username',]
    def get_queryset(self):

        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Create a new attribue"""
        serializer.save(user=self.request.user)

"""
Получение всех заметок
"""
class NoteListView(generics.ListAPIView):
    serializer_class = SecontNoteListSeril
    queryset = Note.objects.all() #Говоряит о том, какие записи мы хотим вынуть
    permission_classes = (IsAuthenticated, )
    def get_queryset(self):
       # its_user = Categoria.objects.filter(creator=self.request.user)
        return self.queryset.filter(user=self.request.user)

"""
Получение конкретной заметки редактором
"""
class NoteDetailViewEditor(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NoteDetailSerilEditor
    queryset = Note.objects.all()
    permission_classes = (IsAuthenticated, IsEditorNote)

    # def get_queryset(self):
    #     return self.queryset.filter(editor=self.request.user)

"""
Получение конкретной заметки создателем
"""
class NoteDetailViewCreator(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SecontNoteDetailSeril
    queryset = Note.objects.all()
    permission_classes = (IsAuthenticated, IsCreaterNote)




