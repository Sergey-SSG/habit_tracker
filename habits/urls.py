from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import HabitViewSet, PublicHabitViewSet, TelegramChatViewSet

router = DefaultRouter()
router.register(r"my_habits", HabitViewSet, basename="my_habits")
router.register(r"public_habits", PublicHabitViewSet, basename="public_habits")
router.register(r"telegram_chats", TelegramChatViewSet, basename="telegram_chats")

urlpatterns = [
    path("", include(router.urls)),
]
