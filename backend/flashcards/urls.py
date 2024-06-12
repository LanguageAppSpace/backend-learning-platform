from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import LessonViewSet, PhrasePairUpdateView, PhrasePairDeleteView


router = DefaultRouter()
router.register(r"lessons", LessonViewSet)

app_name = "flashcards"

urlpatterns = [
    path("", include(router.urls)),
    path(
        "<int:lesson_id>/pairs/<int:pair_id>/",
        PhrasePairUpdateView.as_view(),
        name="pair-update",
    ),
    path(
        "<int:lesson_id>/pairs/<int:pair_id>/delete/",
        PhrasePairDeleteView.as_view(),
        name="pair-delete",
    ),
]
