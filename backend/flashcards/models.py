from django.db import models
from typing import Union
from user.models import CustomUser


class Lesson(models.Model):
    user = models.ForeignKey(
        CustomUser, related_name="lessons", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f"Title: {self.title}"

    def calculate_progress(self) -> Union[int, float]:
        total_pairs = self.phrase_pairs.count()
        if total_pairs == 0:
            return 0
        learned_pairs = self.phrase_pairs.filter(is_learned=True).count()
        return round((learned_pairs / total_pairs) * 100, 2)


class PhrasePair(models.Model):
    lesson = models.ForeignKey(
        Lesson, related_name="phrase_pairs", on_delete=models.CASCADE
    )
    phrase_one = models.CharField(max_length=255)
    phrase_two = models.CharField(max_length=255)
    is_learned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.phrase_one} - {self.phrase_two}"
