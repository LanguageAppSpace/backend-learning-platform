from rest_framework import serializers


class UserStatisticsSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    total_users_count = serializers.IntegerField()
    lessons_count = serializers.IntegerField()
    flashcards_count = serializers.IntegerField()
    learned_flashcards_count = serializers.IntegerField()
