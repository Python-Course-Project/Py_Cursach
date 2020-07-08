from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

"""
Класс Заметки (название заметки, текст заметки, дата публикации и пользователи котрые имеют доступ)
"""

class Note(models.Model):
    note_title = models.CharField(verbose_name='название заметки', max_length=100, blank=True) # Небольшой объём 200-300
    note_text = models.TextField(verbose_name='заметка', blank=False)
    pub_date = models.DateField(verbose_name='дата создания', auto_now=True)
    """
    создатель один - несколько заметок
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, verbose_name='Пользователь',
                             related_name='creator_note')
    """
    Предоставление доступа многим пользователям к многим заметкам
    """
    editor = models.ManyToManyField(User, blank=True, verbose_name='Редактор', related_name='editor_note',
                                 help_text='Вы можете предоставить доступ к вашей заметки', null=True)
    """
    Также в мета можно настроить сортировку вывода данных
    """
    class Meta:
        verbose_name = 'Заметка'
        verbose_name_plural = 'Заметки'
    def __str__(self):
        return  '{0} ({1})'.format(self.note_title, self.pub_date)

"""
Класс Категории заметок (Название категории, заметки)
"""

class Category(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, verbose_name='Создатель',
                                   related_name='creator_categ')
    note_category = models.CharField(verbose_name='категория заметки', max_length=100,
                                  blank=False, unique=True)  # Небольшой объём 200-300
    my_note = models.ManyToManyField(Note, verbose_name='Заметки', blank=True, null=True, related_name='notes')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
    def __str__(self):
        return '{0} ({1}) ({2})'.format(self.note_category, self.creator.username, self.my_note.note_title,
                                        self.my_note.note_text, self.my_note.editor)

