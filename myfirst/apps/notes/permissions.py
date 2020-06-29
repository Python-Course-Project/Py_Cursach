from rest_framework import permissions

""""
Проверяем права ползователя
"""
class IsCreater(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # if request.method in permissions.SAFE_METHODS: #Проверка является ли метод запрооса безопасным : get head options
        #     return True
            return obj.creator == request.user #проверка равен ли пользователь сесси пользователю записи

class IsCreaterOrEditor(permissions.BasePermission):
    def __init__(self, allowed_methods):
        super().__init__()
        self.allowed_methods = allowed_methods

    def has_permission(self, request, view):
        return request.method in self.allowed_methods

    def has_object_permission(self, request, view, obj):
        if obj.editor.filter(username=request.user):
            return True
        return obj.user == request.user


# class CanChangeIt(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         if request.method in permissions.SAFE_METHODS: #Проверка является ли метод запрооса безопасным : get head options
#             return True
#         return obj.creator == request.user #проверка равен ли пользователь сесси пользователю записи