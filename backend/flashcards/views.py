from django.http import Http404

from rest_framework import viewsets, generics, status
from rest_framework.response import Response

from .models import Lesson, PhrasePair
from .serializers import LessonSerializer, PhrasePairSerializer


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    http_method_names = ["get", "post", "delete", "head", "options", "patch"]


class PhrasePairUpdateView(generics.UpdateAPIView):
    queryset = PhrasePair.objects.all()
    serializer_class = PhrasePairSerializer
    http_method_names = ["patch", "head", "options"]

    def get_object(self):
        lesson_id = self.kwargs["lesson_id"]
        pair_id = self.kwargs["pair_id"]
        try:
            return self.queryset.get(id=pair_id, lesson_id=lesson_id)
        except PhrasePair.DoesNotExist:
            raise Http404("Phrase pair does not exist.")


class PhrasePairDeleteView(generics.DestroyAPIView):
    queryset = PhrasePair.objects.all()

    def get_object(self):
        lesson_id = self.kwargs["lesson_id"]
        pair_id = self.kwargs["pair_id"]
        try:
            return self.queryset.get(id=pair_id, lesson_id=lesson_id)
        except PhrasePair.DoesNotExist:
            raise Http404("Phrase pair does not exist.")

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
