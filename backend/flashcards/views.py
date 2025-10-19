from django.http import Http404

from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from user.models import CustomUser
from .models import Lesson, PhrasePair, Section
from .serializers import LessonSerializer, PhrasePairSerializer, \
    SectionSerializer


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    http_method_names = ["get", "post", "delete", "head", "options", "patch"]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Lesson.objects.filter(user=self.request.user.id)

    def perform_create(self, serializer):
        user = self.request.user
        section = serializer.validated_data.get("section")

        if section is None:
            section, _ = Section.objects.get_or_create(
                user=user,
                title="Other",
                defaults={
                    "description": "Default section for unassigned lessons"},
            )

        serializer.save(user=user, section=section)

    def perform_update(self, serializer):
        user_id = self.request.user.id
        user = CustomUser.objects.get(id=user_id)
        serializer.save(user=user)


class PhrasePairUpdateView(generics.UpdateAPIView):
    queryset = PhrasePair.objects.all()
    serializer_class = PhrasePairSerializer
    http_method_names = ["patch", "head", "options"]

    def get_object(self):
        lesson_id = self.kwargs["lesson_id"]
        pair_id = self.kwargs["pair_id"]
        try:
            return self.queryset.get(id=pair_id, lesson_id=lesson_id)
        except PhrasePair.DoesNotExist as exc:
            raise Http404("Phrase pair does not exist.") from exc


class PhrasePairDeleteView(generics.DestroyAPIView):
    queryset = PhrasePair.objects.all()
    serializer_class = PhrasePairSerializer

    def get_object(self):
        lesson_id = self.kwargs["lesson_id"]
        pair_id = self.kwargs["pair_id"]
        try:
            return self.queryset.get(id=pair_id, lesson_id=lesson_id)
        except PhrasePair.DoesNotExist as exc:
            raise Http404("Phrase pair does not exist.") from exc

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "delete", "head", "options", "patch"]

    def get_queryset(self):
        return Section.objects.filter(user=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["get"], url_path="flashcards")
    def get_flashcards(self, request, pk=None):
        """
        Return all flashcards across all lessons in this section.
        """
        section = self.get_object()
        flashcards = section.get_all_phrase_pairs()
        serializer = PhrasePairSerializer(flashcards, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)