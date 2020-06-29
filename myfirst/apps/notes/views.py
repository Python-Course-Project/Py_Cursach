from django.http import HttpResponse
from rest_framework import viewsets, generics
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .permissions import IsCreater, IsCreaterOrEditor
from rest_framework.permissions import IsAuthenticated
from .models import Note, Categoria
from .serializers import SecontNoteDetailSeril, SecontNoteListSeril, CategoriaListSeril,\
    CategoriaDetailSeril, CreateNoteSeril, NoteDetailSerilEditor
from functools import partial
from django.db.models import Q
from django.contrib.auth import get_user_model
User = get_user_model()


"""
Категории
"""
class CategoriaCreateView(generics.CreateAPIView):
    serializer_class = CategoriaDetailSeril
    queryset = Categoria.objects.all()
    permission_classes = (IsAuthenticated, IsCreater)


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


# Создание заметки
class NoteCreateView(generics.CreateAPIView):
    serializer_class = CreateNoteSeril
    permission_classes = (IsAuthenticated, )
    queryset = Note.objects.all()
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Create a new attribue"""
        serializer.save(user=self.request.user)

# Получение всех заметок
class NoteListView(generics.ListAPIView):
    serializer_class = SecontNoteListSeril
    queryset = Note.objects.all() #Говоряит о том, какие записи мы хотим вынуть
    permission_classes = (IsAuthenticated, )
    def get_queryset(self):
       # its_user = Categoria.objects.filter(creator=self.request.user)
        return self.queryset.filter(user=self.request.user)

# Получение конкретной заметки (изменение, удаление и т д)
class NoteDetailView(generics.RetrieveUpdateDestroyAPIView): # RetrieveUpdateDestroyAPIView -
    # позволяет обновлять получать удалять данные об одном объекте
    serializer_class = SecontNoteDetailSeril
    queryset = Note.objects.all()
    permission_classes = (IsAuthenticated, partial(IsCreaterOrEditor, ['GET', 'HEAD', 'PUT', 'PATCH', 'OPTIONS',
                                                                       'POST', 'CONNECT']))
    # def get_queryset(self): # Возвращает объект только для аутентифицированного пользователя
    #  #   self.kwargs['pk']
    #     return self.queryset.filter(user=self.kwargs['user'])

    def get_serializer_class(self):

        serializer_class = self.serializer_class
        if self.request.method == 'PUT':
            if self.queryset.filter(editor=self.request.user).exclude(user=self.request.user):
                serializer_class = NoteDetailSerilEditor
        return serializer_class

    # def get_queryset(self):
    #     # its_user = Categoria.objects.filter(creator=self.request.user)
    #     return self.queryset.filter(user=self.request.user)




