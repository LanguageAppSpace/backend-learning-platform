from datetime import timedelta

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from .models import Lesson, PhrasePair, Section
from .repetition_service import mark_incorrect, schedule_next_review

User = get_user_model()


class LessonViewSetTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
        )
        self.client.force_login(self.user)

        self.lesson_data = {
            "title": "Sample Lesson",
            "description": "A sample lesson description",
            "phrase_pairs": [
                {"phrase_one": "Hello", "phrase_two": "Hola"},
                {"phrase_one": "Goodbye", "phrase_two": "Adiós"},
                {"phrase_one": "Thank you", "phrase_two": "Gracias"},
                {"phrase_one": "Please", "phrase_two": "Por favor"},
                {"phrase_one": "Yes", "phrase_two": "Sí"},
            ],
        }

        self.lesson = Lesson.objects.create(
            title="Existing Lesson",
            description="Existing lesson description",
            user=self.user,
        )

        self.phrase_pair = PhrasePair.objects.create(
            lesson=self.lesson,
            phrase_one="Good Morning",
            phrase_two="Buenos Días",
        )

    def test_create_lesson(self):
        url = reverse("flashcards:lesson-list")
        response = self.client.post(url, self.lesson_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)
        self.assertEqual(PhrasePair.objects.count(), 6)

    def test_get_lesson_list(self):
        url = reverse("flashcards:lesson-list")
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_get_lesson_detail(self):
        url = reverse(
            "flashcards:lesson-detail",
            kwargs={"pk": self.lesson.id},
        )
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.lesson.title)

    def test_delete_lesson(self):
        url = reverse(
            "flashcards:lesson-detail",
            kwargs={"pk": self.lesson.id},
        )
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)
        self.assertEqual(PhrasePair.objects.count(), 0)

    def test_lesson_progress(self):
        lesson = Lesson.objects.create(
            title="Progress Lesson",
            description="A lesson to test progress",
            user=self.user,
        )

        phrases = [
            {
                "phrase_one": "Phrase 1",
                "phrase_two": "Frase 1",
                "is_learned": True,
            },
            {
                "phrase_one": "Phrase 2",
                "phrase_two": "Frase 2",
                "is_learned": True,
            },
            {
                "phrase_one": "Phrase 3",
                "phrase_two": "Frase 3",
                "is_learned": False,
            },
            {
                "phrase_one": "Phrase 4",
                "phrase_two": "Frase 4",
                "is_learned": False,
            },
            {
                "phrase_one": "Phrase 5",
                "phrase_two": "Frase 5",
                "is_learned": False,
            },
        ]

        for phrase in phrases:
            PhrasePair.objects.create(
                lesson=lesson,
                phrase_one=phrase["phrase_one"],
                phrase_two=phrase["phrase_two"],
                is_learned=phrase["is_learned"],
            )

        url = reverse(
            "flashcards:lesson-detail",
            kwargs={"pk": lesson.id},
        )
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["progress"], 40)


class PhrasePairUpdateViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
        )

        self.lesson = Lesson.objects.create(
            title="Lesson with PhrasePair",
            description="Lesson description",
            user=self.user,
        )

        self.phrase_pair = PhrasePair.objects.create(
            lesson=self.lesson,
            phrase_one="Yes",
            phrase_two="Sí",
        )

        self.client.force_login(self.user)

    def test_update_phrase_pair(self):
        url = reverse(
            "flashcards:pair-update",
            kwargs={
                "lesson_id": self.lesson.id,
                "pair_id": self.phrase_pair.id,
            },
        )

        response = self.client.patch(
            url,
            {
                "phrase_one": "No",
                "phrase_two": "No",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.phrase_pair.refresh_from_db()

        self.assertEqual(self.phrase_pair.phrase_one, "No")
        self.assertEqual(self.phrase_pair.phrase_two, "No")

    def test_marking_card_as_learned_schedules_review(self):
        url = reverse(
            "flashcards:pair-update",
            kwargs={
                "lesson_id": self.lesson.id,
                "pair_id": self.phrase_pair.id,
            },
        )

        before_request = timezone.now()

        response = self.client.patch(
            url,
            {"is_learned": True},
            format="json",
        )

        after_request = timezone.now()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.phrase_pair.refresh_from_db()

        self.assertTrue(self.phrase_pair.is_learned)
        self.assertEqual(self.phrase_pair.review_stage, 1)
        self.assertIsNotNone(self.phrase_pair.last_reviewed)
        self.assertIsNotNone(self.phrase_pair.next_review)

        expected_min = before_request + timedelta(days=1)
        expected_max = after_request + timedelta(days=1)

        self.assertGreaterEqual(
            self.phrase_pair.next_review,
            expected_min,
        )
        self.assertLessEqual(
            self.phrase_pair.next_review,
            expected_max,
        )

    def test_already_learned_card_is_not_rescheduled(self):
        first_review_time = timezone.now() - timedelta(hours=2)
        first_next_review = timezone.now() + timedelta(days=3)

        self.phrase_pair.is_learned = True
        self.phrase_pair.review_stage = 2
        self.phrase_pair.last_reviewed = first_review_time
        self.phrase_pair.next_review = first_next_review
        self.phrase_pair.save()

        url = reverse(
            "flashcards:pair-update",
            kwargs={
                "lesson_id": self.lesson.id,
                "pair_id": self.phrase_pair.id,
            },
        )

        response = self.client.patch(
            url,
            {"is_learned": True},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.phrase_pair.refresh_from_db()

        self.assertEqual(self.phrase_pair.review_stage, 2)
        self.assertEqual(self.phrase_pair.last_reviewed, first_review_time)
        self.assertEqual(self.phrase_pair.next_review, first_next_review)


class PhrasePairDeleteViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
        )

        self.lesson = Lesson.objects.create(
            title="Lesson with PhrasePair",
            description="Lesson description",
            user=self.user,
        )

        self.phrase_pair = PhrasePair.objects.create(
            lesson=self.lesson,
            phrase_one="Yes",
            phrase_two="Sí",
        )

        self.client.force_login(self.user)

    def test_delete_phrase_pair(self):
        url = reverse(
            "flashcards:pair-delete",
            kwargs={
                "lesson_id": self.lesson.id,
                "pair_id": self.phrase_pair.id,
            },
        )

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(PhrasePair.objects.count(), 0)


class RepetitionServiceTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="password",
        )

        self.lesson = Lesson.objects.create(
            title="Lesson",
            description="Description",
            user=self.user,
        )

        self.card = PhrasePair.objects.create(
            lesson=self.lesson,
            phrase_one="Hello",
            phrase_two="Hola",
        )

    def test_schedule_next_review(self):
        before = timezone.now()

        schedule_next_review(self.card)

        after = timezone.now()

        self.card.refresh_from_db()

        self.assertEqual(self.card.review_stage, 1)
        self.assertIsNotNone(self.card.last_reviewed)
        self.assertIsNotNone(self.card.next_review)

        self.assertGreaterEqual(
            self.card.last_reviewed,
            before,
        )
        self.assertLessEqual(
            self.card.last_reviewed,
            after,
        )

        self.assertGreaterEqual(
            self.card.next_review,
            before + timedelta(days=1),
        )
        self.assertLessEqual(
            self.card.next_review,
            after + timedelta(days=1),
        )

    def test_mark_incorrect(self):
        self.card.review_stage = 4
        self.card.save()

        before = timezone.now()

        mark_incorrect(self.card)

        after = timezone.now()

        self.card.refresh_from_db()

        self.assertEqual(self.card.review_stage, 0)
        self.assertIsNotNone(self.card.last_reviewed)
        self.assertIsNotNone(self.card.next_review)

        self.assertGreaterEqual(
            self.card.next_review,
            before + timedelta(days=1),
        )
        self.assertLessEqual(
            self.card.next_review,
            after + timedelta(days=1),
        )


class SectionReviewViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            password="password",
        )
        self.client.force_login(self.user)

        self.section = Section.objects.create(
            user=self.user,
            title="Spanish",
            description="Spanish vocabulary",
        )

        self.lesson = Lesson.objects.create(
            user=self.user,
            section=self.section,
            title="Basic Spanish",
            description="Basic phrases",
        )

        self.due_card = PhrasePair.objects.create(
            lesson=self.lesson,
            phrase_one="Hello",
            phrase_two="Hola",
            is_learned=True,
            review_stage=1,
            next_review=timezone.now() - timedelta(minutes=5),
        )

        self.future_card = PhrasePair.objects.create(
            lesson=self.lesson,
            phrase_one="Goodbye",
            phrase_two="Adiós",
            is_learned=True,
            review_stage=1,
            next_review=timezone.now() + timedelta(days=1),
        )

        self.unlearned_card = PhrasePair.objects.create(
            lesson=self.lesson,
            phrase_one="Thank you",
            phrase_two="Gracias",
            is_learned=False,
            next_review=timezone.now() - timedelta(minutes=5),
        )

    def test_review_returns_due_cards(self):
        url = reverse(
            "flashcards:section-review",
            kwargs={"pk": self.section.id},
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        self.assertEqual(
            response.data[0]["id"],
            self.due_card.id,
        )

    def test_review_does_not_return_future_cards(self):
        url = reverse(
            "flashcards:section-review",
            kwargs={"pk": self.section.id},
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        returned_ids = [card["id"] for card in response.data]

        self.assertNotIn(
            self.future_card.id,
            returned_ids,
        )

    def test_review_does_not_return_unlearned_cards(self):
        url = reverse(
            "flashcards:section-review",
            kwargs={"pk": self.section.id},
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        returned_ids = [card["id"] for card in response.data]

        self.assertNotIn(
            self.unlearned_card.id,
            returned_ids,
        )

    def test_review_returns_empty_list_when_no_cards_are_due(self):
        self.due_card.next_review = timezone.now() + timedelta(days=1)
        self.due_card.save(update_fields=["next_review"])

        url = reverse(
            "flashcards:section-review",
            kwargs={"pk": self.section.id},
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])
