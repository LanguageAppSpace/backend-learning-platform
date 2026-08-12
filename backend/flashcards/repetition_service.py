from datetime import timedelta

from django.utils import timezone

REVIEW_INTERVALS = [1, 3, 7, 14, 30, 60]


def schedule_next_review(card):
    stage = min(card.review_stage, len(REVIEW_INTERVALS) - 1)

    card.last_reviewed = timezone.now()
    card.next_review = timezone.now() + timedelta(days=REVIEW_INTERVALS[stage])

    if card.review_stage < len(REVIEW_INTERVALS) - 1:
        card.review_stage += 1

    card.save(
        update_fields=[
            "review_stage",
            "last_reviewed",
            "next_review",
        ]
    )


def mark_incorrect(card):
    card.review_stage = 0
    card.last_reviewed = timezone.now()
    card.next_review = timezone.now() + timedelta(days=1)
    card.save(
        update_fields=[
            "review_stage",
            "last_reviewed",
            "next_review",
        ]
    )
