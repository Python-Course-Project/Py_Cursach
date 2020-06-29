from rest_framework import serializers
from .models import Note, Categoria
from django.contrib.auth import get_user_model
User = get_user_model()

"""
Сериализаторы для категорий
"""

class MyNoteSeril(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        user = self.context['request'].user
        queryset = Note.objects.filter(user=user)
        return queryset

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

class CategoriaListSeril(serializers.ModelSerializer): #Вывод каких-то полей
    my_note = MyNoteSeril(many=True)
    class Meta:
        model = Categoria
        fields = '__all__'

"""
Сериализаторы для заметок
"""
# class NoteSeril(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['username',]
#
#     def get_queryset(self):
#         user = self.context['request'].user
#         queryset = Note.objects.context(user=user)
#         return queryset

class CreateNoteSeril(serializers.ModelSerializer):

    # def __init__(self, *args, **kwargs):
    #     super(CreateNoteSeril, self).__init__(*args, **kwargs)
    #     if 'request' in self.context:
    #         self.fields['editor'].child_relation.queryset = \
    #             self.fields['editor'].child_relation.queryset.exclude(editor=self.context['view'].request.user)
   # editor = NoteSeril(many=True)
    class Meta:
        model = Note
        fields = '__all__'
        read_only_fields = ('user', )

class NoteDetailSerilEditor(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('note_text', )
        read_only_fields = ('note_title', 'pub_date', 'editor', 'user')

class SecontNoteDetailSeril(serializers.ModelSerializer): #Вывод всех полей
   # creator = serializers.HiddenField(default=serializers.CurrentUserDefault())
   # category = CategoriaDetailSeril(many=True, read_only=True)
   # editor = ChoseOfUsers(many=True)
    class Meta:
        model = Note
        fields = ('note_title', 'note_text', 'pub_date', 'editor')
        read_only_fields = ('user', )


class SecontNoteListSeril(serializers.ModelSerializer): #Вывод каких-то полей
    class Meta:
        model = Note
        fields = '__all__'


