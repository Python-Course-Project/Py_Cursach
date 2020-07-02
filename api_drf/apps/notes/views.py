from rest_framework import generics
from .permissions import IsCreater, IsCreaterNote, IsEditorNote
from rest_framework.permissions import IsAuthenticated
from .models import Note, Category
from .serializers import SecontNoteDetailSeril,\
    SecontNoteListSeril,\
    CategoryListSeril,\
    CategoryDetailSeril,\
    CreateNoteSeril,\
    NoteDetailSerilEditor
from django.contrib.auth import get_user_model
User = get_user_model()

"""
Категории
"""
class CategoryCreateView(generics.CreateAPIView):
    serializer_class = CategoryDetailSeril
    queryset = Category.objects.all()
    permission_classes = (IsAuthenticated, IsCreater)

class CategoryListView(generics.ListAPIView):
    serializer_class = CategoryListSeril
    queryset = Category.objects.all() #Говоряит о том, какие записи мы хотим вынуть
    permission_classes = (IsAuthenticated, IsCreater)

    def get_queryset(self):
        return self.queryset.filter(creator=self.request.user)

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView): #позволяет обновлять получать удалять данные об одном объекте
    serializer_class = CategoryDetailSeril
    queryset = Category.objects.all()
    permission_classes = (IsCreater, IsAuthenticated, )


"""
Создание заметки
"""
class NoteCreateView(generics.CreateAPIView):
    serializer_class = CreateNoteSeril
    permission_classes = (IsAuthenticated, )
    queryset = Note.objects.all()

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
        return self.queryset.filter(user=self.request.user)

"""
Получение конкретной заметки редактором
"""
class NoteDetailViewEditor(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NoteDetailSerilEditor
    queryset = Note.objects.all()
    permission_classes = (IsAuthenticated, IsEditorNote)


"""
Получение конкретной заметки создателем
"""
class NoteDetailViewCreator(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SecontNoteDetailSeril
    queryset = Note.objects.all()
    permission_classes = (IsAuthenticated, IsCreaterNote)




