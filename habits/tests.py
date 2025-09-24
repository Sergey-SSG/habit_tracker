from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Habit

User = get_user_model()


class HabitModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@user.com", password="testpass123", username="testuser"
        )

    def test_habit_creation(self):
        habit = Habit.objects.create(
            user=self.user,
            place="Парк",
            time="07:00:00",
            action="Бегать 10 минут",
            duration=120,
        )
        self.assertEqual(habit.action, "Бегать 10 минут")
        self.assertFalse(habit.is_pleasant)

    def test_pleasant_habit_validation(self):
        """Тест валидации приятной привычки."""
        habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="20:00:00",
            action="Читать книгу",
            is_pleasant=True,
            duration=60,
        )
        # У приятной привычки не должно быть вознаграждения или связанной привычки
        self.assertIsNone(habit.reward)
        self.assertIsNone(habit.related_habit)


class HabitAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@user.com", password="testpass123", username="testuser"
        )
        self.client.force_authenticate(user=self.user)

    def test_create_habit(self):
        url = "/api/my_habits/"
        data = {
            "place": "Парк",
            "time": "07:00:00",
            "action": "Бегать 10 минут",
            "duration": 120,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["action"], "Бегать 10 минут")

    def test_get_public_habits(self):
        url = "/api/public_habits/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
