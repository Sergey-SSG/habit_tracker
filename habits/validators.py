from rest_framework import serializers


class HabitValidator:
    """Валидатор для проверки логики модели Habit."""

    def __call__(self, attrs):
        is_pleasant = attrs.get("is_pleasant")
        related_habit = attrs.get("related_habit")
        reward = attrs.get("reward")

        # 1. Исключить одновременный выбор связанной привычки и указания вознаграждения.
        if related_habit and reward:
            raise serializers.ValidationError(
                "Нельзя указывать одновременно связанную привычку и вознаграждение."
            )

        # 2. В связанные привычки могут попадать только привычки с признаком приятной привычки.
        if related_habit and not related_habit.is_pleasant:
            raise serializers.ValidationError(
                "В связанные привычки можно добавлять только приятные привычки."
            )

        # 3. У приятной привычки не может быть вознаграждения или связанной привычки.
        if is_pleasant:
            if reward or related_habit:
                raise serializers.ValidationError(
                    "У приятной привычки не может быть вознаграждения или связанной привычки."
                )

        return attrs
