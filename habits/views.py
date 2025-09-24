from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import Habit, TelegramChat
from .permissions import IsOwner, IsTelegramChatOwner
from .serializers import HabitSerializer, PublicHabitSerializer, TelegramChatSerializer


class HabitPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 50


class HabitViewSet(viewsets.ModelViewSet):
    """ViewSet для привычек текущего пользователя."""

    serializer_class = HabitSerializer
    pagination_class = HabitPagination
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["is_pleasant", "is_public"]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PublicHabitViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для публичных привычек."""

    serializer_class = PublicHabitSerializer
    pagination_class = HabitPagination
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Habit.objects.filter(is_public=True)


class TelegramChatViewSet(viewsets.ModelViewSet):
    """ViewSet для Telegram чатов."""

    serializer_class = TelegramChatSerializer
    permission_classes = [permissions.IsAuthenticated, IsTelegramChatOwner]

    def get_queryset(self):
        return TelegramChat.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["post"])
    def verify(self, request):
        """Эндпоинт для верификации Telegram чата."""
        chat_id = request.data.get("chat_id")
        # verification_code = request.data.get("verification_code")

        # Здесь должна быть логика верификации через бот
        # Для примера упрощенная версия
        try:
            chat = TelegramChat.objects.get(chat_id=chat_id, user=request.user)
            chat.verified = True
            chat.save()
            return Response({"status": "Chat verified successfully"})
        except TelegramChat.DoesNotExist:
            return Response(
                {"error": "Chat not found"}, status=status.HTTP_404_NOT_FOUND
            )
