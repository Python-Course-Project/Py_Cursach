from rest_framework import serializers
from .models import Note, Category
from django.contrib.auth import get_user_model
User = get_user_model()

"""
 Позволяет получить только заметки пользователя для добавления в категории
"""
class MyNoteSeril(serializers.PrimaryKeyRelatedField):  #PrimaryKeyRelatedField
    def get_queryset(self):
        user = self.context['request'].user
        queryset = Note.objects.filter(user=user)
        return queryset

"""
 Вывод какой-то категории
"""
class CategoryDetailSeril(serializers.ModelSerializer): #Вывод всех полей (первая строчка - запрет на изменение пользователя)
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())
    my_note = MyNoteSeril(many=True)

    class Meta:
        model = Category
        fields = '__all__'
        #read_only_fields = ('my_note_isadded', )
"""
 Форматирования вывода заметок в категориях
"""
class NoteLisForCat(serializers.ModelSerializer): #Вывод всех заметок
    class Meta:
        model = Note
        fields = ('note_title', 'pub_date')

"""
 Вывод всех категорий
"""
class CategoryListSeril(serializers.ModelSerializer):
    my_note = NoteLisForCat(many=True)
    class Meta:
        model = Category
        fields = '__all__'
"""
Сериализаторы для заметок
"""

"""
Позволяет в editor исключить самого пользователя
"""
class EditorWithoutUser(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        user = self.context['request'].user
        queryset = User.objects.exclude(username=user).exclude(is_superuser=True)
        return queryset

"""
Создание заметки
"""
class CreateNoteSeril(serializers.ModelSerializer):
    editor = EditorWithoutUser(many=True)
    class Meta:
        model = Note
        fields = '__all__'
        read_only_fields = ('user', )

"""
Получение конкретно заметки Редактором
"""
class NoteDetailSerilEditor(serializers.ModelSerializer):
    editor = EditorWithoutUser(many=True)
    class Meta:
        model = Note
        fields = ('note_text', )
        read_only_fields = ('note_title', 'pub_date', 'editor', 'user')


"""
Получение конкретно заметки Создателем
"""
class SecontNoteDetailSeril(serializers.ModelSerializer): #Вывод всех полей
    editor = EditorWithoutUser(many=True)
    class Meta:
        model = Note
        fields = ('note_title', 'note_text', 'pub_date', 'editor', )
        read_only_fields = ('user',)

"""
Получение списка заметок
"""
class SecontNoteListSeril(serializers.ModelSerializer): #Вывод всех заметок
    class Meta:
        model = Note
        fields = '__all__'



