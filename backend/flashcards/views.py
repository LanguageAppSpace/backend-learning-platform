from django.http import Http404

from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from user.models import CustomUser
from .models import Lesson, PhrasePair
from .serializers import LessonSerializer, PhrasePairSerializer


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    http_method_names = ["get", "post", "delete", "head", "options", "patch"]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Lesson.objects.filter(user=self.request.user.id)

    def perform_create(self, serializer):
        user_id = self.request.user.id
        user = CustomUser.objects.get(id=user_id)
        serializer.save(user=user)

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
