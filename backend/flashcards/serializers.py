from rest_framework import serializers

from .models import Lesson, PhrasePair


class PhrasePairSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhrasePair
        fields = ["id", "phrase_one", "phrase_two"]


class LessonSerializer(serializers.ModelSerializer):
    phrase_pairs = PhrasePairSerializer(many=True)

    class Meta:
        model = Lesson
        fields = ["id", "title", "description", "phrase_pairs"]

    def create(self, validated_data):
        phrase_pairs_data = validated_data.pop("phrase_pairs", [])
        lesson = Lesson.objects.create(**validated_data)
        for phrase_pair_data in phrase_pairs_data:
            PhrasePair.objects.create(lesson=lesson, **phrase_pair_data)
        return lesson

    def update(self, instance, validated_data):
        phrase_pairs_data = validated_data.pop("phrase_pairs", None)

        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.save()

        if phrase_pairs_data is not None:
            for phrase_pair_data in phrase_pairs_data:
                if "id" in phrase_pair_data:
                    try:
                        phrase_pair = PhrasePair.objects.get(
                            id=phrase_pair_data["id"], lesson=instance
                        )
                        phrase_pair.phrase_one = phrase_pair_data.get(
                            "phrase_one", phrase_pair.phrase_one
                        )
                        phrase_pair.phrase_two = phrase_pair_data.get(
                            "phrase_two", phrase_pair.phrase_two
                        )
                        phrase_pair.save()
                    except PhrasePair.DoesNotExist:
                        PhrasePair.objects.create(lesson=instance, **phrase_pair_data)
                else:
                    PhrasePair.objects.create(lesson=instance, **phrase_pair_data)

        return instance
