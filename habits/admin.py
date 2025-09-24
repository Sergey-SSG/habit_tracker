from django.contrib import admin

from .models import Habit, TelegramChat


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ("action", "user", "time", "place", "is_pleasant", "is_public")
    list_filter = ("is_pleasant", "is_public", "periodicity")
    search_fields = ("action", "place", "user__email")
    readonly_fields = ("last_reminder_sent",)


@admin.register(TelegramChat)
class TelegramChatAdmin(admin.ModelAdmin):
    list_display = ("user", "chat_id", "verified", "created_at")
    list_filter = ("verified",)
    search_fields = ("user__email", "chat_id")
