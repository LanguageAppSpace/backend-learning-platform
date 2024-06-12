from django.db import models


class Lesson(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title


class PhrasePair(models.Model):
    lesson = models.ForeignKey(
        Lesson, related_name="phrase_pairs", on_delete=models.CASCADE
    )
    phrase_one = models.CharField(max_length=255)
    phrase_two = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.phrase_one} - {self.phrase_two}"
