from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from user.models import CustomUser


class Section(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        CustomUser, related_name="sections", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"Section: {self.title}"

    def calculate_progress(self):
        """
        Calculate average progress across all lessons in this section.
        """
        lessons = self.lessons.all()
        if not lessons.exists():
            return 0
        total_progress = sum(lesson.calculate_progress() for lesson in lessons)
        return round(total_progress / lessons.count(), 2)

    def get_all_phrase_pairs(self):
        """
        Fetch all phrase pairs across all lessons in this section.
        """
        return PhrasePair.objects.filter(lesson__section=self)


class Lesson(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        CustomUser, related_name="lessons", on_delete=models.CASCADE
    )
    section = models.ForeignKey(
        Section, related_name="lessons", on_delete=models.CASCADE, null=True,
        blank=True
    )
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f"Lesson title: {self.title}"

    def calculate_progress(self):
        total_pairs = self.phrase_pairs.count()
        if total_pairs == 0:
            return 0
        learned_pairs = self.phrase_pairs.filter(is_learned=True).count()
        return round((learned_pairs / total_pairs) * 100, 2)


class PhrasePair(models.Model):
    id = models.AutoField(primary_key=True)
    lesson = models.ForeignKey(
        Lesson, related_name="phrase_pairs", on_delete=models.CASCADE
    )
    phrase_one = models.CharField(max_length=255)
    phrase_two = models.CharField(max_length=255)
    is_learned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.phrase_one} - {self.phrase_two}"


@receiver(post_save, sender=CustomUser)
def create_default_section(sender, instance, created, **kwargs):
    if created:
        Section.objects.get_or_create(
            user=instance,
            title="Other",
            defaults={"description": "Default section for unassigned lessons"},
        )
