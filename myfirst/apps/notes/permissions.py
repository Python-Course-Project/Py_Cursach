from rest_framework import permissions

""""
Проверяем права ползователя
"""
class IsCreater(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # if obj.creator == request.user and obj.get(pk=obj.my_note).exist():
        #     return True
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


# class IsCreaterOrEditor(permissions.BasePermission):
#     def __init__(self, allowed_methods):
#         super().__init__()
#         self.allowed_methods = allowed_methods
#
#
#     def has_permission(self, request, view):
#         return request.method in self.allowed_methods
#
#     def has_object_permission(self, request, view, obj):
#        delete = 'DELETE'
#        if obj.editor.filter(username=request.user):
#            if delete in self.allowed_methods:
#                self.allowed_methods.remove(delete)
#            return True
#        elif obj.user == request.user:
#            if delete not in self.allowed_methods:
#                self.allowed_methods.append(delete)
#            return True
