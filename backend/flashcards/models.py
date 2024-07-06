from django.db import models


class Lesson(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f"Title: {self.title}"

    def calculate_progress(self):
        total_pairs = self.phrase_pairs.count()
        if total_pairs == 0:
            return 0
        learned_pairs = self.phrase_pairs.filter(is_learned=True).count()
        return (learned_pairs / total_pairs) * 100


class PhrasePair(models.Model):
    lesson = models.ForeignKey(
        Lesson, related_name="phrase_pairs", on_delete=models.CASCADE
    )
    phrase_one = models.CharField(max_length=255)
    phrase_two = models.CharField(max_length=255)
    is_learned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.phrase_one} - {self.phrase_two}"
