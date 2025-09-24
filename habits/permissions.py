from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """Разрешение на изменение только своих привычек."""

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsTelegramChatOwner(permissions.BasePermission):
    """Разрешение на доступ только к своему Telegram чату."""

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
