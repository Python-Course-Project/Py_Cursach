from rest_framework import permissions

""""
Проверяем права ползователя
"""
class IsCreater(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
      return obj.creator == request.user #проверка равен ли пользователь сесси пользователю записи


class IsCreaterNote(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
            return obj.user == request.user

class IsEditorNote(permissions.BasePermission):

    def __init__(self):
        super().__init__()
        self.allowed_methods = ['GET', 'HEAD', 'PUT', 'PATCH', 'OPTIONS',
                                                                       'POST', 'CONNECT']
    def has_object_permission(self, request, view, obj):
        return obj.editor.filter(username=request.user)

    def has_permission(self, request, view):
        return request.method in self.allowed_methods
