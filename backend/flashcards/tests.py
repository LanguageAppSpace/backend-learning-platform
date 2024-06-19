from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from .models import Lesson, PhrasePair


User = get_user_model()


class LessonViewSetTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.lesson_data = {
            "title": "Sample Lesson",
            "description": "A sample lesson description",
            "phrase_pairs": [
                {"phrase_one": "Hello", "phrase_two": "Hola"},
                {"phrase_one": "Goodbye", "phrase_two": "Adiós"},
            ],
        }
        self.lesson = Lesson.objects.create(
            title="Existing Lesson", description="Existing lesson description"
        )
        self.phrase_pair = PhrasePair.objects.create(
            lesson=self.lesson, phrase_one="Good Morning", phrase_two="Buenos Días"
        )

    def test_create_lesson(self):
        url = reverse("flashcards:lesson-list")
        self.client.force_login(self.user)
        response = self.client.post(url, self.lesson_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)
        self.assertEqual(PhrasePair.objects.count(), 3)

    def test_get_lesson_list(self):
        url = reverse("flashcards:lesson-list")
        self.client.force_login(self.user)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_get_lesson_detail(self):
        url = reverse("flashcards:lesson-detail", kwargs={"pk": self.lesson.id})
        self.client.force_login(self.user)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.lesson.title)

    def test_delete_lesson(self):
        url = reverse("flashcards:lesson-detail", kwargs={"pk": self.lesson.id})
        self.client.force_login(self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)
        self.assertEqual(PhrasePair.objects.count(), 0)


class PhrasePairUpdateViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.lesson = Lesson.objects.create(
            title="Lesson with PhrasePair", description="Lesson description"
        )
        self.phrase_pair = PhrasePair.objects.create(
            lesson=self.lesson, phrase_one="Yes", phrase_two="Sí"
        )
        self.update_data = {"phrase_one": "No", "phrase_two": "No"}

    def test_update_phrase_pair(self):
        url = reverse(
            "flashcards:pair-update",
            kwargs={"lesson_id": self.lesson.id, "pair_id": self.phrase_pair.id},
        )
        self.client.force_login(self.user)
        response = self.client.patch(url, self.update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.phrase_pair.refresh_from_db()
        self.assertEqual(self.phrase_pair.phrase_one, "No")
        self.assertEqual(self.phrase_pair.phrase_two, "No")


class PhrasePairDeleteViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.lesson = Lesson.objects.create(
            title="Lesson with PhrasePair", description="Lesson description"
        )
        self.phrase_pair = PhrasePair.objects.create(
            lesson=self.lesson, phrase_one="Yes", phrase_two="Sí"
        )

    def test_delete_phrase_pair(self):
        url = reverse(
            "flashcards:pair-delete",
            kwargs={"lesson_id": self.lesson.id, "pair_id": self.phrase_pair.id},
        )
        self.client.force_login(self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(PhrasePair.objects.count(), 0)
