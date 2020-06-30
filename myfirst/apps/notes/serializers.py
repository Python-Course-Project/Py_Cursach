from rest_framework import serializers
from .models import Note, Categoria
from django.contrib.auth import get_user_model
User = get_user_model()
from rest_marshmallow import Schema, fields

"""
Сериализаторы для категорий
"""

class UserSchema(Schema):
    username = fields.String()
    password = fields.String(dump_only=True)
    class Meta:
        model = User
        fields = ('username', 'password')

class NoteSchema(Schema):
    note_title = fields.String()
    note_text = fields.String()
    pub_date = fields.Date()
    user = fields.Nested(UserSchema, dump_only=True)
    editor = fields.Nested(UserSchema)

class CategoriaSchema(Schema):
    creator = fields.Nested(UserSchema, dump_only=True)
    note_categoria = fields.String()
    my_note = fields.Nested(NoteSchema)
    class Meta:
        model = Categoria
        fields = ('creator', 'note_categoria', 'my_note')

full_serial = CategoriaSchema()

"""
 Позволяет получить только заметки пользователя для добавления в категории
"""
class MyNoteSeril(serializers.PrimaryKeyRelatedField):  #PrimaryKeyRelatedField
    def get_queryset(self):
        user = self.context['request'].user
        # onl_user_notes = Note.objects.filter(user=user)
        # queryset = Categoria.objects.exclude(my_note=onl_user_notes)
        queryset = Note.objects.filter(user=user, isadded=False)
        return queryset

"""
 Вывод какой-то категории
"""
class CategoriaDetailSeril(serializers.ModelSerializer): #Вывод всех полей (первая строчка - запрет на изменение пользователя)
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())
    my_note = MyNoteSeril(many=True)
    # def create(self, validated_data): # Не помогает
    #     validated_data['my_note'] = Note.objects.filter(user=self.context['view'].request.user)
    #     return super(CategoriaDetailSeril, self).create(validated_data)
    #


    # """
    # Позволяет ограничить выборку заметок для добавления в категорию (только заметки пользователя)
    # """
    # def __init__(self, *args, **kwargs): # Не помогает
    #     super(CategoriaDetailSeril, self).__init__(*args, **kwargs)
    #     if 'request' in self.context:
    #         self.fields['my_note'].queryset = Note.objects.filter(categoria__my_note__user=self.context['view'].request.user)

    # def get_fields(self, *args, **kwargs):
    #     fields = super(CategoriaDetailSeril, self).get_fields(*args, **kwargs)
    #     view = self.context['view']
    #     user_id = view.kwargs.get('user')
    #     fields['my_note'].queryset = fields['my_note'].queryset.filter(user=user_id)
    #     return fields

    class Meta:
        model = Categoria
        fields = '__all__'

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
class CategoriaListSeril(serializers.ModelSerializer):
    my_note = NoteLisForCat(many=True)
    class Meta:
        model = Categoria
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
        queryset = User.objects.exclude(username=user)
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
    class Meta:
        model = Note
        fields = ('note_text', )
        read_only_fields = ('note_title', 'pub_date', 'editor', 'user')


"""
Получение конкретно заметки Создателем
"""
class SecontNoteDetailSeril(serializers.ModelSerializer): #Вывод всех полей
    class Meta:
        model = Note
        fields = ('note_title', 'note_text', 'pub_date', 'editor')
        read_only_fields = ('user', )

"""
Получение списка заметок
"""
class SecontNoteListSeril(serializers.ModelSerializer): #Вывод всех заметок
    class Meta:
        model = Note
        fields = '__all__'



