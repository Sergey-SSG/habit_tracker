from rest_framework import serializers

from .models import Habit, TelegramChat
from .validators import HabitValidator


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор для привычек."""

    related_habit = serializers.PrimaryKeyRelatedField(
        queryset=Habit.objects.filter(is_pleasant=True), required=False, allow_null=True
    )

    class Meta:
        model = Habit
        fields = [
            "id",
            "user",
            "place",
            "time",
            "action",
            "is_pleasant",
            "related_habit",
            "periodicity",
            "reward",
            "duration",
            "is_public",
            "last_reminder_sent",
        ]
        read_only_fields = ("user", "last_reminder_sent")

    def validate(self, data):
        HabitValidator()(data)
        return data

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class TelegramChatSerializer(serializers.ModelSerializer):
    """Сериализатор для Telegram чатов."""

    class Meta:
        model = TelegramChat
        fields = ["id", "user", "chat_id", "verified", "created_at"]
        read_only_fields = ("user", "verified", "created_at")


class PublicHabitSerializer(serializers.ModelSerializer):
    """Сериализатор для публичных привычек."""

    user_email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Habit
        fields = [
            "id",
            "user_email",
            "place",
            "time",
            "action",
            "periodicity",
            "duration",
            "is_public",
        ]
        read_only_fields = fields
