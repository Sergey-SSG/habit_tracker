import telegram
from celery import shared_task
from django.conf import settings
from django.utils import timezone

from .models import Habit


@shared_task
def send_telegram_reminder(habit_id):
    """Отправка напоминания о привычке в Telegram."""
    try:
        habit = Habit.objects.get(id=habit_id)
        user = habit.user

        # Проверяем, есть ли у пользователя привязанный и верифицированный чат
        if not hasattr(user, "telegram_chat") or not user.telegram_chat.verified:
            return

        bot = telegram.Bot(token=settings.TELEGRAM_BOT_TOKEN)
        message = (
            f"🔔 Напоминание о привычке!\n\n"
            f"📍 Место: {habit.place}\n"
            f"⏰ Время: {habit.time.strftime('%H:%M')}\n"
            f"🎯 Действие: {habit.action}\n"
            f"⏱️ Время на выполнение: {habit.duration} секунд\n"
            f"📅 Периодичность: {habit.get_periodicity_display()}"
        )

        if habit.reward:
            message += f"\n🎁 Вознаграждение: {habit.reward}"
        elif habit.related_habit:
            message += f"\n😊 Приятная привычка: {habit.related_habit.action}"

        bot.send_message(chat_id=user.telegram_chat.chat_id, text=message)

        # Обновляем время последнего напоминания
        habit.last_reminder_sent = timezone.now()
        habit.save()

    except Habit.DoesNotExist:
        print(f"Habit with id {habit_id} does not exist")
    except telegram.error.TelegramError as e:
        print(f"Telegram error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


@shared_task
def schedule_habits():
    """Периодическая задача для планирования напоминаний."""
    now = timezone.now()
    current_time = now.time().replace(second=0, microsecond=0)

    # Находим привычки, для которых нужно отправить напоминание
    habits = Habit.objects.all()

    for habit in habits:
        # Проверяем время привычки (без секунд)
        habit_time = habit.time.replace(second=0, microsecond=0)

        if habit_time != current_time:
            continue

        # Проверяем периодичность
        if habit.last_reminder_sent:
            days_passed = (now.date() - habit.last_reminder_sent.date()).days
            if days_passed < habit.periodicity:
                continue

        # Отправляем напоминание
        send_telegram_reminder.delay(habit.id)
