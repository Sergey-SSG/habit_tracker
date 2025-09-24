from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Habit(models.Model):
    PERIODICITY_CHOICES = [
        (1, "Ежедневно"),
        (2, "Раз в два дня"),
        (3, "Раз в три дня"),
        (4, "Раз в четыре дня"),
        (5, "Раз в пять дней"),
        (6, "Раз в шесть дней"),
        (7, "Раз в неделю"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="пользователь"
    )
    place = models.CharField(max_length=255, verbose_name="место")
    time = models.TimeField(verbose_name="время")
    action = models.CharField(max_length=255, verbose_name="действие")
    is_pleasant = models.BooleanField(
        default=False, verbose_name="признак приятной привычки"
    )
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="связанная привычка",
    )
    periodicity = models.PositiveSmallIntegerField(
        choices=PERIODICITY_CHOICES,
        default=1,
        verbose_name="периодичность (в днях)",
        validators=[MinValueValidator(1), MaxValueValidator(7)],
    )
    reward = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="вознаграждение"
    )
    duration = models.PositiveIntegerField(
        verbose_name="время на выполнение (в секундах)",
        validators=[MinValueValidator(1), MaxValueValidator(120)],
        help_text="Продолжительность должна быть не более 120 секунд.",
    )
    is_public = models.BooleanField(default=False, verbose_name="признак публичности")
    last_reminder_sent = models.DateTimeField(
        null=True, blank=True, verbose_name="последнее напоминание"
    )

    def __str__(self):
        return f"Я буду {self.action} в {self.time} в {self.place}"

    class Meta:
        verbose_name = "привычка"
        verbose_name_plural = "привычки"
        ordering = ["id"]


class TelegramChat(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="telegram_chat"
    )
    chat_id = models.BigIntegerField(unique=True)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat {self.chat_id} for {self.user.email}"

    class Meta:
        verbose_name = "Telegram чат"
        verbose_name_plural = "Telegram чаты"
