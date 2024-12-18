from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from flashcards.models import Lesson, PhrasePair
from user.models import CustomUser


class UserStatisticsView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = None

    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        user = CustomUser.objects.get(id=user_id)
        lessons_count = Lesson.objects.filter(user=user).count()
        flashcards_count = PhrasePair.objects.filter(lesson__user=user).count()
        learned_flashcards_count = PhrasePair.objects.filter(
            lesson__user=user, is_learned=True
        ).count()
        total_users_count = CustomUser.objects.count()
        user_stats = {
            "username": user.username,
            "total_users_count": total_users_count,
            "lessons_count": lessons_count,
            "flashcards_count": flashcards_count,
            "learned_flashcards_count": learned_flashcards_count,
        }

        return Response(user_stats, status=status.HTTP_200_OK)
